# LMStudio Monitor — Documentación Técnica

Panel de control TUI en tiempo real para monitorear los logs del servidor
LMStudio, implementado en Python con la biblioteca `rich`.

## Instalación

### Requisitos previos

- Python 3.10 o superior
- Biblioteca `rich`

```bash
pip install rich
```

## Arquitectura

### Estructura del módulo

```
lmstudio-monitor.py
├── Configuración de themes
│   ├── THEME_ACTUAL          # Theme por defecto
│   ├── THEMES                # Paletas de colores predefinidas
│   └── SIMBOLOS             # Símbolos Unicode para la interfaz
├── Constantes
│   ├── RUTA_BASE_LOGS_DEFAULT  # Ruta raíz de logs
│   └── PATRONES             # Expresiones regulares para parsing
├── Funciones
│   ├── estado_inicial()     # Devuelve diccionario de estado inicial
│   ├── obtener_theme()      # Devuelve la paleta de colores
│   ├── buscar_ultimo_log()  # Localiza el log más reciente
│   └── construir_panel()    # Genera la interfaz Rich
├── Clases
│   └── LectorLog            # Lector de logs con tailing incremental
└── principal()              # Punto de entrada
```

### Flujo de ejecución

1. **Inicialización**: se parsean los argumentos, se localiza el archivo de log
   y se crea una instancia de `LectorLog`.
2. **Bucle principal**: cada `intervalo` segundos:
   - Se busca si hay un nuevo archivo de log (rotación diaria).
   - Se leen solo las líneas nuevas del archivo (tailing incremental).
   - Se actualiza el estado acumulado con las nuevas líneas.
   - Se construye y actualiza el panel visual.
3. **Terminación**: se cierra al presionar `q` o `Ctrl+C`.

### Clase LectorLog

La clase `LectorLog` gestiona la lectura incremental de archivos de log y es la
pieza central del monitor:

```python
class LectorLog:
    def __init__(self):
        self.ruta = None          # Ruta del archivo actual
        self.offset = 0           # Posición de lectura (bytes)
        self.estado = estado_inicial()  # Estado acumulado
        self.errores_recientes = []     # Últimos 5 errores
        self.marca_tiempo = "-"         # Última marca de tiempo

    def leer_nuevas_lineas(self, ruta_archivo: Path) -> list:
        # Lee solo líneas nuevas desde self.offset
        # Resetea el estado si el archivo cambió
        ...

    def actualizar_estado(self, lineas: list) -> dict:
        # Procesa líneas nuevas y actualiza self.estado
        ...
```

**Características principales:**

- **Tailing incremental**: usa `seek()` para leer solo desde la última posición
  conocida, sin releer el archivo completo en cada ciclo.
- **Detección de rotación**: resetea el estado cuando cambia la ruta del archivo.
- **Acumulación de estado**: mantiene el estado entre iteraciones sin
  reconstruirlo desde cero.
- **Manejo de errores**: si el archivo no existe, marca `error_lectura` en el
  estado (sin crashear) y el bucle principal muestra un panel de espera.

## Sistema de themes

### Themes disponibles

| Theme | Estilo | Colores principales |
| --- | --- | --- |
| `dracula` | Vibrante sobre fondo oscuro | Púrpura, cyan, verde |
| `nord` | Frío y profesional | Azules, cyan, verdes |
| `minimalista` | Limpio y neutro | Grises con acento azul |

### Estructura de un theme

```python
THEMES = {
    "nombre_theme": {
        "fondo": "on #282a36",        # Color de fondo
        "texto": "#f8f8f2",           # Color de texto principal
        "primario": "#bd93f9",        # Bordes, títulos
        "secundario": "#8be9fd",      # Valores, claves
        "terciario": "#50fa7b",       # Acentos, progreso
        "apagado": "#6272a4",         # Texto secundario
        "estado_activo": "#50fa7b",   # Verde para activo
        "estado_detenido": "#ff5555", # Rojo para detenido
        "estado_advertencia": "#f1fa8c",  # Amarillo para advertencia
        "borde_panel": "#bd93f9",     # Color de bordes
        "error": "#ff5555",           # Color de errores
    }
}
```

### Símbolos Unicode

```python
SIMBOLOS = {
    "activo": "●",        # Estado activo
    "detenido": "○",      # Estado detenido
    "advertencia": "◆",   # Advertencia/desconocido
    "barra_llena": "█",   # Barra de progreso llena
    "barra_vacia": "░",   # Barra de progreso vacía
    "titulo": "◆",        # Decoración de títulos
    "error": "✗",         # Errores
    "separador": "·",     # Separadores
    "streaming": "▶",     # Streaming activo
}
```

### Crear un theme personalizado

Añadir una entrada al diccionario `THEMES`:

```python
THEMES["mi_theme"] = {
    "fondo": "on #1a1b26",
    "texto": "#c0caf5",
    "primario": "#7aa2f7",
    "secundario": "#7dcfff",
    "terciario": "#9ece6a",
    "apagado": "#565f89",
    "estado_activo": "#9ece6a",
    "estado_detenido": "#f7768e",
    "estado_advertencia": "#e0af68",
    "borde_panel": "#7aa2f7",
    "error": "#f7768e",
}
```

Luego ejecutar con:

```bash
python3 lmstudio-monitor.py --theme mi_theme
```

### Cambiar theme por defecto

Editar la línea al inicio del script:

```python
THEME_ACTUAL = "mi_theme"  # Cambiar aquí el theme por defecto
```

## Parsing de logs

El sistema de parsing utiliza expresiones regulares definidas en `PATRONES`
para extraer información clave:

| Patrón | Descripción | Datos extraídos |
| --- | --- | --- |
| `servidor_iniciado` | Inicio del servidor | — |
| `servidor_detenido` | Detención del servidor | — |
| `servidor_escuchando` | Puerto de escucha | Puerto |
| `modelo_cargando` | Carga de modelo | Ruta del archivo |
| `modelo_cargado` | Modelo cargado | Booleano |
| `modelo_slots` | Configuración de slots | num_slots, contexto_por_slot |
| `progreso_prompt` | Progreso de procesamiento | Porcentaje |
| `velocidad_procesamiento_prompt` | Velocidad de procesamiento | tokens, velocidad |
| `evaluacion_prompt` | Evaluación de prompt | tiempo, tokens, velocidad |
| `evaluacion_generacion` | Evaluación de generación | tiempo, tokens, velocidad |
| `tiempo_total` | Tiempo total | tiempo_ms, tokens |
| `chat_ejecutando` | Chat en ejecución | Número de mensajes |
| `streaming_inicio` / `streaming_fin` | Transmisión | Booleano |
| `peticion_recibida` | Nueva petición | Método, endpoint |
| `error` | Errores detectados | Línea de error |

> Nota: el patrón `evaluacion_generacion` usa un *lookbehind* negativo
> (`(?<!prompt )`) para no colisionar con `evaluacion_prompt`, y el patrón
> `error` es `r"ERROR|error|failed"` con `re.IGNORECASE`.

## Modelo de datos

El estado del servidor se almacena en un diccionario con las siguientes claves:

```python
estado = {
    # Servidor
    "estado_servidor": str,      # "Activo" | "Detenido" | "Desconocido"
    "puerto_servidor": str,      # Puerto de escucha
    "ultima_peticion": str,      # Marca de tiempo
    "endpoint_ultima_peticion": str,  # Método + ruta

    # Modelo
    "nombre_modelo": str,        # Nombre del modelo
    "archivo_modelo": str,       # Archivo GGUF
    "modelo_cargado": bool,      # Estado de carga
    "num_slots": str,            # Número de slots
    "contexto_por_slot": str,    # Tokens por slot

    # Procesamiento de prompt
    "progreso_prompt": float,    # Porcentaje (0-100)
    "progreso_prompt_activo": bool,
    "tokens_prompt": int,
    "velocidad_prompt": float,   # tokens/segundo

    # Evaluación de prompt
    "tiempo_eval_prompt": float, # milisegundos
    "tokens_eval_prompt": int,
    "velocidad_eval_prompt": float,
    "ultima_eval_prompt": dict | None,  # {"tiempo", "tokens", "velocidad"}

    # Generación
    "tiempo_eval_generacion": float,
    "tokens_eval_generacion": int,
    "velocidad_eval_generacion": float,
    "ultima_eval_generacion": dict | None,  # {"tiempo", "tokens", "velocidad"}

    # Totales
    "tiempo_total_ms": float,
    "tokens_totales": int,
    "ultimo_total": dict | None,  # {"tiempo", "tokens"}

    # Streaming
    "transmitiendo": bool,
    "chat_ejecutandose": bool,
    "mensajes_chat": int,

    # Errores
    "errores": list[tuple[str, str]],  # [(marca_tiempo, mensaje), ...]

    # Metadatos
    "archivo_log": str,
    "lineas_log": int,
    "error_lectura": str | None,  # Mensaje de error si no se puede leer el log
}
```

## Estructura de logs

### Ubicación

```
~/.lmstudio/server-logs/
├── 2026-01/
│   ├── 2026-01-01.1.log
│   ├── 2026-01-01.2.log
│   └── ...
├── 2026-02/
└── ...
```

### Formato

- **Directorios mensuales**: `YYYY-MM/`
- **Archivos diarios**: `YYYY-MM-DD.N.log` (N = número de rotación)
- **Formato de línea**: `[YYYY-MM-DD HH:MM:SS][NIVEL][ORIGEN] mensaje`

### Ejemplo de línea de log

```
[2026-09-08 14:32:15][INFO][llama.cpp] model loaded
```

## Interfaz de usuario

### Secciones del panel

| Sección | Contenido |
| --- | --- |
| **Servidor** | Estado, puerto, última petición, endpoint |
| **Modelo** | Nombre, archivo GGUF, slots, contexto por slot |
| **Procesamiento de Prompt** | Barra de progreso, tokens, velocidad |
| **Generación** | Tokens generados, velocidad tok/s |
| **Última Petición** | Tokens de prompt, generación, tiempo total |
| **Errores** | Últimos 5 errores con marca de tiempo |

## Desarrollo

### Dependencias

- Python 3.10+
- `rich`

### Extensión de patrones

Para añadir nuevos patrones de parsing, editar el diccionario `PATRONES`:

```python
PATRONES = {
    # ... patrones existentes ...
    "nuevo_patron": re.compile(r"expresión regular"),
}
```

Y procesarlos en el método `actualizar_estado()` de la clase `LectorLog`:

```python
coincidencia = PATRONES["nuevo_patron"].search(linea)
if coincidencia:
    self.estado["nueva_clave"] = coincidencia.group(1)
```

### Añadir nuevas secciones al panel

1. Crear una tabla Rich en `construir_panel()`.
2. Usar los colores del theme: `theme['primario']`, `theme['secundario']`, etc.
3. Usar los símbolos de `SIMBOLOS` para mantener consistencia.
4. Añadirla al layout correspondiente.
5. Actualizar el modelo de datos en `estado_inicial()` y el parsing en
   `LectorLog.actualizar_estado()`.

```python
# Crear tabla con colores del theme
tabla = Table(show_header=False, box=None, padding=(0, 1))
tabla.add_column("Clave", style=f"bold {theme['secundario']}", width=14)
tabla.add_column("Valor", style=theme['texto'])

# Usar símbolos consistentes
tabla.add_row("Estado", f"{SIMBOLOS['activo']} Activo")

# Añadir al layout
layout["seccion"].split_row(
    Layout(Panel(tabla, title=f"[bold {theme['primario']}]Título[/bold {theme['primario']}]", border_style=theme['borde_panel']), ratio=1),
)
```

## Historial de correcciones

Resultado de una revisión de código (2026-09-09), ya implementada en el script:

1. **Colisión de regex prompt/generación** (crítico): el patrón
   `evaluacion_generacion` ahora usa lookbehind negativo `(?<!prompt )` para no
   capturar las líneas de "prompt eval time".
2. **Crash si el log no existe** (alto): el lector devuelve siempre el estado
   completo y marca `error_lectura`; el bucle principal muestra un panel de
   espera en lugar de cerrarse con `KeyError`.
3. **Tailing incremental** (alto): se mantiene el estado acumulado y se lee con
   `seek()` solo lo nuevo, evitando releer el archivo completo cada tick.
4. **Duplicación de líneas cabecera/cola** (medio): resuelta de forma natural
   por el tailing incremental.
5. **Regex de `error`** (bajo): simplificada a `r"ERROR|error|failed"` con
   `re.IGNORECASE`, eliminando la heurística de estilo logcat.

## Solución de problemas

### El monitor no encuentra logs

```bash
ls -la ~/.lmstudio/server-logs/
```

Si están en otra ubicación, usar `--logs-dir`.

### Rendimiento

- **Tailing incremental**: solo se leen las líneas nuevas, eficiente incluso con
  logs de varios MB.
- **Detección de rotación**: al cambiar el archivo (rotación diaria), se resetea
  y empieza a leer desde el principio del nuevo archivo.
- **Gestión de errores**: si el log no existe, muestra un aviso y espera a que
  esté disponible sin cerrarse.

## Licencia

Uso interno — Proyecto personal.
