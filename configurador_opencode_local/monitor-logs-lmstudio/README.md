# LMStudio Monitor

Panel de control en tiempo real (TUI) para monitorizar los logs del servidor
de **LMStudio** desde la terminal. Muestra de un vistazo el estado del
servidor, el modelo cargado y las métricas de procesamiento y generación de
tokens.

## Qué muestra

- **Servidor**: estado (activo/detenido/desconocido), puerto de escucha,
  última petición recibida y endpoint.
- **Modelo**: nombre, archivo GGUF, número de slots y contexto por slot.
- **Procesamiento de prompt**: barra de progreso, tokens procesados y velocidad.
- **Generación**: tokens generados, tiempo y velocidad (tok/s).
- **Última petición completada**: tokens y velocidad de prompt y generación.
- **Errores recientes**: los últimos 5 errores con su marca de tiempo.

## Requisitos

- Python 3.10 o superior
- Biblioteca `rich`

```bash
pip install rich
```

## Uso

```bash
python3 lmstudio-monitor.py
```

### Opciones

| Opción | Descripción | Por defecto |
| --- | --- | --- |
| `--interval N` | Intervalo de actualización en segundos | `2` |
| `--file RUTA` | Monitorizar un archivo de log concreto | Auto-detecta el más reciente |
| `--logs-dir DIR` | Directorio raíz de logs | `~/.lmstudio/server-logs` |
| `--theme THEME` | Tema de colores (`dracula`, `nord`, `minimalista`) | `dracula` |
| `--help`, `-h` | Muestra la ayuda | — |

### Ejemplos

```bash
# Actualización cada 5 segundos
python3 lmstudio-monitor.py --interval 5

# Un archivo de log concreto
python3 lmstudio-monitor.py --file ~/.lmstudio/server-logs/2026-09/2026-09-08.1.log

# Directorio de logs personalizado
python3 lmstudio-monitor.py --logs-dir /ruta/personalizada/server-logs

# Con el tema Nord
python3 lmstudio-monitor.py --theme nord

# En segundo plano
nohup python3 lmstudio-monitor.py > /dev/null 2>&1 &
```

### Atajos de teclado

| Tecla | Acción |
| --- | --- |
| `q` | Salir del monitor |
| `Ctrl+C` | Forzar la salida |

## Temas disponibles

| Tema | Estilo |
| --- | --- |
| `dracula` | Vibrante sobre fondo oscuro |
| `nord` | Frío y profesional |
| `minimalista` | Limpio y neutro |

Para cambiar el tema por defecto, edita la variable `THEME_ACTUAL` al inicio
del script.

## Solución de problemas

- **No encuentra logs**: comprueba que existe `~/.lmstudio/server-logs/`. Si
  están en otra ubicación, usa `--logs-dir`.
- **Errores de codificación**: el script los maneja automáticamente.
- **Log grande**: usa *tailing* incremental, así que solo lee las líneas nuevas
  en cada ciclo (no relee el archivo completo).

## Otros scripts de la carpeta

- `lmstudio_sincerts.sh`: lanza la AppImage de LMStudio desactivando la
  verificación TLS de Node (`NODE_TLS_REJECT_UNAUTHORIZED=0`).

La documentación técnica detallada está en [DOCUMENTACION.md](DOCUMENTACION.md).
