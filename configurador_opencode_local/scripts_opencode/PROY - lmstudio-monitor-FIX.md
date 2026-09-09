---
version: 1.0
fecha: 2026-09-09
estado: ACTIVO
descripcion: Roadmap de correcciones y mejoras detectadas en lmstudio-monitor.py durante una revisión de código, para que otro agente las implemente y verifique.
tipo: roadmap
autor: Claude (revisión de código)
---

# PROY — Correcciones lmstudio-monitor.py

## Objetivo

Este documento recoge los hallazgos de una revisión de código sobre
`lmstudio-monitor.py` (panel TUI en tiempo real para logs de LMStudio).
Cada punto incluye: prioridad, ubicación, problema, causa raíz, propuesta
de solución y cómo verificar que quedó resuelto. El agente que lo aborde
puede trabajar los puntos en el orden en que aparecen (de mayor a menor
prioridad) y marcar cada uno como ✅ al terminarlo.

## Resumen de estado

| # | Ítem | Prioridad | Estado |
|---|------|-----------|--------|
| 1 | Colisión de regex prompt/generación | 🔴 crítico | ✅ completado |
| 2 | Crash si el log no existe | 🟡 alto | ✅ completado |
| 3 | Re-lectura completa del log en cada tick (no hay tailing incremental) | 🟡 alto | ✅ completado |
| 4 | Duplicación de líneas cabecera/cola | 🟢 medio | ✅ completado |
| 5 | Regex de `error` con heurística ajena (estilo logcat) | 🔵 bajo | ✅ completado |

---

## 1. 🔴 Colisión entre los patrones `evaluacion_prompt` y `evaluacion_generacion`

**Ubicación:** diccionario `PATRONES`, claves `evaluacion_prompt` (línea ~113) y
`evaluacion_generacion` (línea ~116); se consumen en `parsear_cola_log` (~286-306).

**Problema:** cada vez que aparece una línea de "prompt eval time" en el log,
también hace match el patrón de "eval time" (generación), porque este último
no está anclado y `"eval time ="` es una subcadena de `"prompt eval time ="`.
Confirmado con una prueba directa:

```python
p_prompt = re.compile(r'prompt eval time =\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second')
p_gen    = re.compile(r'eval time =\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second')
linea = 'llama_print_timings: prompt eval time =    50.65 ms /   127 tokens (... 2506.42 tokens per second)'
p_prompt.search(linea)  # -> match (correcto)
p_gen.search(linea)     # -> también match (INCORRECTO)
```

**Efecto:** `tokens_eval_generacion`, `tiempo_eval_generacion` y
`velocidad_eval_generacion` (y su copia en `ultima_eval_generacion`) se
sobrescriben con los datos del *prompt*, no de la generación real. El panel
"Generación" muestra números incorrectos.

**Propuesta:**

```python
"evaluacion_generacion": re.compile(
    r"(?<!prompt )eval time =\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second"
),
```

(lookbehind negativo para excluir explícitamente las líneas que empiezan con
"prompt eval time").

**Verificación:** repetir la prueba de arriba y comprobar que `p_gen.search(linea)`
ya no hace match sobre la línea de "prompt eval time =...". Además, probar
contra una línea real de generación (`... eval time = 1500.00 ms / 100 tokens
(... tokens per second)`, sin la palabra "prompt" delante) y comprobar que sigue
haciendo match ahí.

---

## 2. 🟡 Crash si el archivo de log no existe

**Ubicación:** `parsear_cola_log` (~192-196) y `construir_panel` (~347 en adelante).

**Problema:** si `open()` lanza `FileNotFoundError`, la función devuelve
`{"error": f"Archivo de log no encontrado: {ruta_archivo}"}`, un diccionario
que **solo** tiene esa clave. `construir_panel` asume que `estado` trae todas
las claves del estado completo (`estado["estado_servidor"]`, `estado["puerto_servidor"]`,
etc.), así que en cuanto se le pasa ese dict incompleto lanza `KeyError` y
tumba el bucle `Live` (el monitor se cierra con traceback).

**Propuesta:** que `parsear_cola_log` devuelva siempre el diccionario de
estado completo (con sus valores por defecto), añadiendo simplemente una
clave adicional `estado["error_lectura"] = "..."` cuando corresponda, en vez
de sustituir todo el dict. Alternativa más simple: en `principal()`,
comprobar antes de construir el panel:

```python
estado = parsear_cola_log(archivo_log)
if "error" in estado and len(estado) == 1:
    # mostrar un panel de espera/error en vez de crashear
    en_vivo.update(Panel(f"[bold red]{estado['error']}[/bold red]"))
    time.sleep(intervalo)
    continue
```

**Verificación:** ejecutar el script apuntando con `--file` a una ruta que no
existe y comprobar que el monitor sigue vivo (muestra un aviso) en vez de
cerrarse con `KeyError`.

---

## 3. 🟡 No hay tailing incremental: se relee el fichero completo en cada intervalo

**Ubicación:** `parsear_cola_log` (~192-194), llamada desde el bucle principal
en `principal()` (~566-577).

**Problema:** `archivo.readlines()` carga el archivo **entero** en cada
iteración del bucle (por defecto cada 2 s), y solo después se recorta a
`max_lineas`. Para una sesión larga de LMStudio con un log que crece a lo
largo de horas, esto implica releer megabytes de disco constantemente en vez
de mantener el offset de bytes ya leídos y hacer `seek()` desde ahí. Con
logs pequeños no se nota, pero es justo lo contrario de una monitorización
"en caliente" eficiente, y es el punto que más se aleja del objetivo del
script.

**Propuesta (esquema):** mantener estado acumulado entre iteraciones en vez
de reconstruirlo desde cero cada vez:

```python
class LectorLog:
    def __init__(self):
        self.ruta = None
        self.offset = 0
        self.estado = estado_inicial()  # el dict con los valores por defecto

    def leer_nuevas_lineas(self, ruta_archivo: Path) -> list[str]:
        if ruta_archivo != self.ruta:
            self.ruta = ruta_archivo
            self.offset = 0
            self.estado = estado_inicial()
        with open(ruta_archivo, "r", errors="replace") as f:
            f.seek(self.offset)
            nuevas = f.readlines()
            self.offset = f.tell()
        return nuevas
```

Y luego actualizar `self.estado` in-place solo con las líneas nuevas,
reutilizando la misma lógica de parseo de patrones que ya existe pero sin
reconstruir el diccionario de estado desde cero cada tick.

**Verificación:** con un log grande (varios MB), comprobar que el uso de
CPU/IO del proceso no crece de forma proporcional al tamaño total del
archivo, y que el estado (última petición, errores recientes, etc.) sigue
siendo correcto tras reiniciar el monitor a mitad de sesión.

---

## 4. 🟢 Duplicación de líneas entre cabecera y cola

**Ubicación:** `parsear_cola_log` (~198-203).

```python
if len(lineas) <= max_lineas:
    lineas_combinadas = lineas
else:
    cabecera = lineas[:400]
    cola = lineas[-max_lineas:]
    lineas_combinadas = cabecera + cola
```

**Problema:** si el archivo tiene, por ejemplo, 1600 líneas, la cabecera
(0-399) y la cola (últimas 1500, es decir 100-1599) se solapan en 300
líneas. No rompe el script, pero esas líneas se procesan dos veces — lo más
visible es que un mismo error puede aparecer duplicado en `errores_recientes`
antes del recorte a los últimos 5.

**Propuesta:**

```python
if len(lineas) <= max_lineas:
    lineas_combinadas = lineas
else:
    cola = lineas[-max_lineas:]
    limite_cabecera = max(0, len(lineas) - max_lineas)
    cabecera = lineas[:min(400, limite_cabecera)]
    lineas_combinadas = cabecera + cola
```

**Verificación:** con un archivo de ~1600 líneas con al menos un error
conocido en la zona de solape, comprobar que `errores_recientes` no lo
contiene duplicado.

*Nota: si se implementa el punto 3 (tailing incremental), este problema
desaparece por sí solo y este parche deja de ser necesario.*

---

## 5. 🔵 Regex de `error` con heurística de otro contexto (estilo logcat)

**Ubicación:** `PATRONES["error"]` (línea ~124) y su uso en el bucle de
`parsear_cola_log` (~334-337).

```python
"error": re.compile(r"\bE\b.*|ERROR|error|failed|failed to"),
...
if PATRONES["error"].search(linea) and ("E " in linea or "ERROR" in linea or "error" in linea.lower()):
```

**Problema:** `\bE\b` (letra "E" aislada) es una heurística típica de logcat
de Android (nivel de log "E" = Error), no de los logs de LMStudio/llama.cpp,
y puede producir falsos positivos con cualquier línea que contenga una "E"
suelta como palabra. Además `"failed to"` es redundante (ya lo cubre
`"failed"`), y la comprobación adicional en el `if` repite parte de lo que
ya hace el propio regex.

**Propuesta:**

```python
"error": re.compile(r"ERROR|error|failed", re.IGNORECASE),
```

y simplificar el uso a:

```python
if PATRONES["error"].search(linea):
    linea_limpia = re.sub(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[.*?\]\s*", "", linea).strip()
    if linea_limpia and len(linea_limpia) > 10:
        errores_recientes.append((marca_tiempo, linea_limpia[:90]))
```

**Verificación:** revisar un log real de LMStudio con al menos un error
conocido y confirmar que sigue detectándose, y que líneas normales que
contengan una "E" suelta (p. ej. rutas de Windows, fórmulas) ya no se
marcan como error.

---

## Orden de trabajo sugerido

1. Punto 1 (crítico, corrige datos incorrectos ya visibles).
2. Punto 2 (evita que el monitor se caiga en un caso borde).
3. Punto 3 (mejora estructural más grande; conviene hacerla antes de tocar
   más el parseo, porque cambia dónde vive el estado).
4. Punto 4 (se resuelve solo si se aborda el punto 3; si no, aplicar el
   parche puntual).
5. Punto 5 (limpieza, sin urgencia).

---

## Estado de implementación

Todos los puntos han sido implementados y verificados:

- **Punto 1**: Corregido con lookbehind negativo `(?<!prompt )` en la regex de `evaluacion_generacion`.
- **Punto 2**: Implementado devolviendo siempre el diccionario de estado completo con `error_lectura` cuando corresponde.
- **Punto 3**: Implementado con la clase `LectorLog` que mantiene estado acumulado y usa `seek()` para tailing incremental.
- **Punto 4**: Resuelto automáticamente con el tailing incremental (ya no se procesan líneas duplicadas).
- **Punto 5**: Simplificado a `r"ERROR|error|failed"` con `re.IGNORECASE` y eliminada la condición redundante.

El monitor ahora es más eficiente con logs grandes, maneja errores de archivo correctamente, y muestra datos precisos en el panel de generación.
