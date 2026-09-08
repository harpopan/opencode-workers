# LMStudio Log Monitor — Documentación para Desarrolladores

Panel de control TUI en tiempo real para monitorear los logs del servidor LMStudio.

## Instalación

### Requisitos previos

- Python 3.10 o superior
- Biblioteca `rich` (normalmente preinstalada en sistemas Linux)

```bash
# Instalar dependencias (si no están disponibles)
pip install rich
```

### Configuración

El script se encuentra en:

```
~/.lmstudio/lmstudio-monitor.py
```

## Uso

### Ejecución básica

```bash
python3 ~/.lmstudio/lmstudio-monitor.py
```

### Parámetros de línea de comandos

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `--interval N` | Intervalo de actualización en segundos | `2` |
| `--file PATH` | Ruta a un archivo de log específico | Auto-detecta |
| `--theme THEME` | Theme de colores (dracula, nord, minimalista) | `dracula` |
| `--help, -h` | Muestra la ayuda | — |

### Ejemplos

```bash
# Ejecutar con actualización cada 5 segundos
python3 ~/.lmstudio/lmstudio-monitor.py --interval 5

# Monitorizar un archivo de log específico
python3 ~/.lmstudio/lmstudio-monitor.py --file ~/.lmstudio/server-logs/2026-09/2026-09-08.1.log

# Ejecutar con theme Nord
python3 ~/.lmstudio/lmstudio-monitor.py --theme nord

# Ejecutar en segundo plano
nohup python3 ~/.lmstudio/lmstudio-monitor.py > /dev/null 2>&1 &
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
│   ├── RUTA_BASE_LOGS       # Ruta raíz de logs
│   └── PATRONES             # Expresiones regulares para parsing
├── Funciones
│   ├── obtener_theme()      # Devuelve la paleta de colores
│   ├── buscar_ultimo_log()  # Localiza el log más reciente
│   ├── parsear_cola_log()   # Extrae estado del servidor
│   └── construir_panel()    # Genera la interfaz Rich
└── principal()              # Punto de entrada
```

## Sistema de themes

### Themes disponibles

| Theme | Estilo | Colores principales |
|-------|--------|---------------------|
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

Para crear un nuevo theme, añadir una entrada al diccionario `THEMES`:

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

### Flujo de ejecución

1. **Inicialización**: Se parsean los argumentos y se localiza el archivo de log
2. **Bucle principal**: Cada `intervalo` segundos:
   - Se busca si hay un nuevo archivo de log (rotación diaria)
   - Se parsea el archivo para extraer el estado actual
   - Se construye y actualiza el panel visual
3. **Terminación**: Se cierra al presionar `q` o `Ctrl+C`

### Parsing de logs

El sistema de parsing utiliza expresiones regulares definidas en `PATRONES` para extraer información clave:

| Patrón | Descripción | Datos extraídos |
|--------|-------------|-----------------|
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

### Modelo de datos

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

    # Generación
    "tiempo_eval_generacion": float,
    "tokens_eval_generacion": int,
    "velocidad_eval_generacion": float,

    # Totales
    "tiempo_total_ms": float,
    "tokens_totales": int,

    # Streaming
    "transmitiendo": bool,
    "chat_ejecutandose": bool,
    "mensajes_chat": int,

    # Errores
    "errores": list[tuple[str, str]],  # [(marca_tiempo, mensaje), ...]

    # Metadatos
    "archivo_log": str,
    "lineas_log": int,
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
|---------|-----------|
| **Servidor** | Estado (activo/detenido/desconocido), puerto, última petición, endpoint |
| **Modelo** | Nombre, archivo GGUF, slots, contexto por slot |
| **Procesamiento de Prompt** | Barra de progreso, tokens procesados, velocidad |
| **Generación** | Tokens generados, velocidad tok/s |
| **Última Petición** | Tokens de prompt, tokens de generación, tiempo total |
| **Errores** | Últimos 5 errores con marca de tiempo |

### Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `q` | Salir del monitor |
| `Ctrl+C` | Forzar salida |

## Desarrollo

### Dependencias

- Python 3.10+
- `rich` — Biblioteca para interfaces de terminal enriquecidas

### Extensión de patrones

Para añadir nuevos patrones de parsing, editar el diccionario `PATRONES`:

```python
PATRONES = {
    # ... patrones existentes ...
    "nuevo_patron": re.compile(r"expresión regular"),
}
```

Y procesarlos en `parsear_cola_log()`:

```python
coincidencia = PATRONES["nuevo_patron"].search(linea)
if coincidencia:
    estado["nueva_clave"] = coincidencia.group(1)
```

### Añadir nuevas secciones al panel

Para añadir una nueva sección visual:

1. Crear una tabla Rich en `construir_panel()`
2. Usar los colores del theme: `theme['primario']`, `theme['secundario']`, etc.
3. Usar los símbolos de `SIMBOLOS` para mantener consistencia
4. Añadirla al layout correspondiente
5. Actualizar el modelo de datos en `parsear_cola_log()`

Ejemplo:

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

## Solución de problemas

### El monitor no encuentra logs

Verificar que existe la ruta:

```bash
ls -la ~/.lmstudio/server-logs/
```

### Errores de codificación

El script maneja automáticamente errores de codificación con `errors="replace"`.

### Rendimiento

- Para logs muy grandes (>10000 líneas), se procesan solo las primeras 400 y las últimas 1500 líneas
- El intervalo de actualización por defecto (2s) es equilibrado para la mayoría de casos

## Licencia

Uso interno — Proyecto personal.
