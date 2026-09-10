#!/usr/bin/env python3
"""
Monitor de Logs de LMStudio — Panel de control TUI en tiempo real.

Este módulo monitoriza los archivos de log del servidor LMStudio y muestra
un panel de control interactivo con información sobre el estado del servidor,
el modelo cargado, el progreso de procesamiento y generación de tokens.

Dependencias:
    - rich: Biblioteca para interfaces de terminal enriquecidas

Uso:
    python3 lmstudio-monitor.py [--interval SEGUNDOS] [--file RUTA] [--theme THEME]
                                [--platform auto|linux|windows] [--logs-dir DIR]
    py lmstudio-monitor.py [--interval SEGUNDOS] [--file RUTA] [--theme THEME]  (Windows)
                           [--platform auto|linux|windows] [--logs-dir DIR]
"""

import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# En Windows, forzar consola UTF-8 para que los simbolos Unicode (● █ ░ ▶ ◆ ✗)
# no salgan como simbolos raros. En Windows Terminal funciona perfecto;
# en conhost clasico requiere fuente Consolas/Cascadia + chcp 65001.
if os.name == "nt":
    try:
        os.system("chcp 65001 > nul 2>&1")
    except Exception:
        pass
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def _importar_rich():
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    return Console, Layout, Live, Panel, Table, Text, box


try:
    Console, Layout, Live, Panel, Table, Text, box = _importar_rich()
except ModuleNotFoundError:
    print("Falta la dependencia 'rich' (ModuleNotFoundError: No module named 'rich')", file=sys.stderr)
    print("Intentando instalarla automaticamente con pip...", file=sys.stderr)
    instalado = False
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "rich"])
        instalado = True
    except Exception:
        # Si ni siquiera hay pip (tipico en Windows con instalacion minima),
        # intentar restaurarlo con ensurepip y reintentar una vez.
        try:
            print("pip no disponible, intentando restaurarlo con ensurepip...", file=sys.stderr)
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "rich"])
            instalado = True
        except Exception:
            instalado = False
    if instalado:
        try:
            Console, Layout, Live, Panel, Table, Text, box = _importar_rich()
            print("'rich' instalado correctamente. Continuando...", file=sys.stderr)
        except ModuleNotFoundError:
            # pip instalo en otra ubicacion o hace falta reiniciar el proceso
            # (tipico si pip instalo con --user o en entorno roto).
            print("", file=sys.stderr)
            print("'rich' parece haberse instalado, pero este proceso aun no lo ve.", file=sys.stderr)
            print("Vuelve a ejecutar el script:", file=sys.stderr)
            print("  Linux / macOS :  python3 lmstudio-monitor.py --help", file=sys.stderr)
            print("  Windows       :  py lmstudio-monitor.py --help", file=sys.stderr)
            sys.exit(1)
    else:
        print("", file=sys.stderr)
        print("No se pudo instalar 'rich' automaticamente. Instalalo manualmente:", file=sys.stderr)
        print("  Linux / macOS :  pip3 install rich   (o: python3 -m pip install rich)", file=sys.stderr)
        print("  Windows       :  py -m pip install rich", file=sys.stderr)
        print("                   (si 'py' no funciona, prueba: python -m pip install rich)", file=sys.stderr)
        print("  Si falta pip  :  py -m ensurepip --upgrade", file=sys.stderr)
        print("                   py -m pip install rich", file=sys.stderr)
        print("", file=sys.stderr)
        print("Tambien puedes usar requirements.txt:", file=sys.stderr)
        print("  py -m pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

# =============================================================================
# CONFIGURACIÓN DE THEMES
# =============================================================================

# Theme por defecto (cambiar aquí o usar --theme)
THEME_ACTUAL = "dracula"

# Paletas de colores predefinidas
THEMES = {
    "dracula": {
        "fondo": "on #282a36",
        "texto": "#f8f8f2",
        "primario": "#bd93f9",
        "secundario": "#8be9fd",
        "terciario": "#50fa7b",
        "apagado": "#6272a4",
        "estado_activo": "#50fa7b",
        "estado_detenido": "#ff5555",
        "estado_advertencia": "#f1fa8c",
        "borde_panel": "#bd93f9",
        "error": "#ff5555",
    },
    "nord": {
        "fondo": "on #2e3440",
        "texto": "#eceff4",
        "primario": "#81a1c1",
        "secundario": "#88c0d0",
        "terciario": "#a3be8c",
        "apagado": "#4c566a",
        "estado_activo": "#a3be8c",
        "estado_detenido": "#bf616a",
        "estado_advertencia": "#ebcb8b",
        "borde_panel": "#81a1c1",
        "error": "#bf616a",
    },
    "minimalista": {
        "fondo": "on #1e1e2e",
        "texto": "#cdd6f4",
        "primario": "#89b4fa",
        "secundario": "#a6adc8",
        "terciario": "#94e2d5",
        "apagado": "#585b70",
        "estado_activo": "#a6e3a1",
        "estado_detenido": "#f38ba8",
        "estado_advertencia": "#f9e2af",
        "borde_panel": "#89b4fa",
        "error": "#f38ba8",
    },
}

# Símbolos Unicode para la interfaz
SIMBOLOS = {
    "activo": "●",
    "detenido": "○",
    "advertencia": "◆",
    "barra_llena": "█",
    "barra_vacia": "░",
    "titulo": "◆",
    "error": "✗",
    "separador": "·",
    "streaming": "▶",
}

# =============================================================================
# CONSTANTES
# =============================================================================

# Ruta Linux por defecto donde se almacenan los logs del servidor
RUTA_BASE_LOGS_LINUX = Path.home() / ".lmstudio" / "server-logs"

# Ruta Windows por defecto donde se almacenan los logs del servidor
# (equivale a C:\Users\<usuario>\.lmstudio\apps\bionic\server-logs)
RUTA_BASE_LOGS_WINDOWS = Path.home() / ".lmstudio" / "apps" / "bionic" / "server-logs"

# Compatibilidad hacia atrás: antes solo existía la ruta Linux hardcodeada.
RUTA_BASE_LOGS_DEFAULT = RUTA_BASE_LOGS_LINUX


def detectar_ruta_base() -> Path:
    """
    Detecta automáticamente qué directorio base de logs utilizar.

    Orden de preferencia:
      1. Si solo uno de los dos existe, devuelve ese.
      2. Si existen ambos, devuelve el que contenga el *.log más reciente.
      3. Si ninguno existe, devuelve el default según el SO actual
         (Windows -> ruta Windows, resto -> ruta Linux).

    Returns:
        Path: Ruta base de logs detectada.
    """
    linux_existe = RUTA_BASE_LOGS_LINUX.exists()
    windows_existe = RUTA_BASE_LOGS_WINDOWS.exists()

    if linux_existe and not windows_existe:
        return RUTA_BASE_LOGS_LINUX
    if windows_existe and not linux_existe:
        return RUTA_BASE_LOGS_WINDOWS
    if linux_existe and windows_existe:
        try:
            logs_linux = list(RUTA_BASE_LOGS_LINUX.rglob("*.log"))
            logs_windows = list(RUTA_BASE_LOGS_WINDOWS.rglob("*.log"))
            if logs_linux and not logs_windows:
                return RUTA_BASE_LOGS_LINUX
            if logs_windows and not logs_linux:
                return RUTA_BASE_LOGS_WINDOWS
            if logs_linux and logs_windows:
                ultimo_linux = max(p.stat().st_mtime for p in logs_linux)
                ultimo_windows = max(p.stat().st_mtime for p in logs_windows)
                return RUTA_BASE_LOGS_WINDOWS if ultimo_windows >= ultimo_linux else RUTA_BASE_LOGS_LINUX
        except OSError:
            pass
        # Ambos existen pero sin logs (o error leyendo): preferir el nativo del SO.
        return RUTA_BASE_LOGS_WINDOWS if os.name == "nt" else RUTA_BASE_LOGS_LINUX

    # Ninguno existe: devolver el nativo del SO para que el error sea claro.
    return RUTA_BASE_LOGS_WINDOWS if os.name == "nt" else RUTA_BASE_LOGS_LINUX


def resolver_ruta_base(plataforma: str = "auto", logs_dir: str | Path | None = None) -> Path:
    """
    Resuelve el directorio base de logs según plataforma y/o ruta personalizada.

    Args:
        plataforma: 'auto' (detectar), 'linux' o 'windows' ('win' como alias).
        logs_dir: Ruta personalizada (tiene máxima prioridad, equivale a --logs-dir).

    Returns:
        Path: Directorio base de logs a utilizar.
    """
    if logs_dir:
        return Path(logs_dir)
    p = (plataforma or "auto").lower()
    if p == "linux":
        return RUTA_BASE_LOGS_LINUX
    if p in ("windows", "win"):
        return RUTA_BASE_LOGS_WINDOWS
    return detectar_ruta_base()


def estado_inicial() -> dict:
    """
    Devuelve el diccionario de estado inicial con valores por defecto.

    Returns:
        dict: Diccionario con el estado inicial del servidor.
    """
    return {
        "estado_servidor": "Desconocido",
        "puerto_servidor": "-",
        "nombre_modelo": "-",
        "archivo_modelo": "-",
        "modelo_cargado": False,
        "num_slots": "-",
        "contexto_por_slot": "-",
        "progreso_prompt": 0.0,
        "progreso_prompt_activo": False,
        "tokens_prompt": 0,
        "velocidad_prompt": 0.0,
        "tiempo_eval_prompt": 0.0,
        "tokens_eval_prompt": 0,
        "velocidad_eval_prompt": 0.0,
        "tiempo_eval_generacion": 0.0,
        "tokens_eval_generacion": 0,
        "velocidad_eval_generacion": 0.0,
        "tiempo_total_ms": 0.0,
        "tokens_totales": 0,
        "chat_ejecutandose": False,
        "mensajes_chat": 0,
        "transmitiendo": False,
        "ultima_peticion": "-",
        "hora_ultima_peticion": "-",
        "endpoint_ultima_peticion": "-",
        "ultima_eval_prompt": None,
        "ultima_eval_generacion": None,
        "ultimo_total": None,
        "errores": [],
        "archivo_log": "",
        "lineas_log": 0,
        "error_lectura": None,
    }


class LectorLog:
    """
    Lector de logs con tailing incremental.

    Mantiene el estado acumulado entre iteraciones y solo lee las líneas
    nuevas del archivo de log, evitando releer el archivo completo en cada tick.
    """

    def __init__(self):
        """Inicializa el lector de logs."""
        self.ruta = None
        self.offset = 0
        self.estado = estado_inicial()
        self.errores_recientes = []
        self.marca_tiempo = "-"

    def leer_nuevas_lineas(self, ruta_archivo: Path) -> list:
        """
        Lee las líneas nuevas del archivo de log desde la última posición.

        Si el archivo ha cambiado (o es la primera lectura), resetea el estado
        y lee desde el principio.

        Args:
            ruta_archivo: Ruta al archivo de log a leer.

        Returns:
            list: Lista de líneas nuevas leídas.
        """
        if ruta_archivo != self.ruta:
            self.ruta = ruta_archivo
            self.offset = 0
            self.estado = estado_inicial()
            self.errores_recientes = []
            self.marca_tiempo = "-"

        try:
            with open(ruta_archivo, "r", errors="replace") as f:
                f.seek(self.offset)
                nuevas = f.readlines()
                self.offset = f.tell()
                self.estado["error_lectura"] = None
                return nuevas
        except FileNotFoundError:
            self.estado["error_lectura"] = f"Archivo de log no encontrado: {ruta_archivo}"
            return []

    def actualizar_estado(self, lineas: list) -> dict:
        """
        Actualiza el estado con las líneas nuevas leídas.

        Args:
            lineas: Lista de líneas nuevas a procesar.

        Returns:
            dict: Estado actualizado del servidor.
        """
        for linea in lineas:
            coincidencia_ts = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", linea)
            if coincidencia_ts:
                self.marca_tiempo = coincidencia_ts.group(1)

            coincidencia = PATRONES["servidor_escuchando"].search(linea)
            if coincidencia:
                self.estado["puerto_servidor"] = coincidencia.group(1)
                self.estado["estado_servidor"] = "Activo"

            if PATRONES["servidor_iniciado"].search(linea):
                self.estado["estado_servidor"] = "Activo"
            if PATRONES["servidor_detenido"].search(linea):
                self.estado["estado_servidor"] = "Detenido"

            coincidencia = PATRONES["modelo_cargando"].search(linea)
            if coincidencia:
                self.estado["archivo_modelo"] = Path(coincidencia.group(1)).name
                ruta_completa = coincidencia.group(1)
                partes = ruta_completa.split("/")
                if len(partes) >= 3:
                    self.estado["nombre_modelo"] = "/".join(partes[-2:])
                else:
                    self.estado["nombre_modelo"] = Path(ruta_completa).name

            if PATRONES["modelo_cargado"].search(linea):
                self.estado["modelo_cargado"] = True

            coincidencia = PATRONES["modelo_slots"].search(linea)
            if coincidencia:
                self.estado["num_slots"] = coincidencia.group(1)
                self.estado["contexto_por_slot"] = coincidencia.group(2)

            coincidencia = PATRONES["progreso_prompt"].search(linea)
            if coincidencia:
                porcentaje = float(coincidencia.group(1))
                self.estado["progreso_prompt"] = porcentaje
                self.estado["progreso_prompt_activo"] = porcentaje < 100.0

            coincidencia = PATRONES["velocidad_procesamiento_prompt"].search(linea)
            if coincidencia:
                self.estado["tokens_prompt"] = int(coincidencia.group(1))
                self.estado["velocidad_prompt"] = float(coincidencia.group(3))

            coincidencia = PATRONES["evaluacion_prompt"].search(linea)
            if coincidencia:
                self.estado["tiempo_eval_prompt"] = float(coincidencia.group(1))
                self.estado["tokens_eval_prompt"] = int(coincidencia.group(2))
                self.estado["velocidad_eval_prompt"] = float(coincidencia.group(3))
                self.estado["ultima_eval_prompt"] = {
                    "tiempo": float(coincidencia.group(1)),
                    "tokens": int(coincidencia.group(2)),
                    "velocidad": float(coincidencia.group(3)),
                }

            coincidencia = PATRONES["evaluacion_generacion"].search(linea)
            if coincidencia:
                self.estado["tiempo_eval_generacion"] = float(coincidencia.group(1))
                self.estado["tokens_eval_generacion"] = int(coincidencia.group(2))
                self.estado["velocidad_eval_generacion"] = float(coincidencia.group(3))
                self.estado["ultima_eval_generacion"] = {
                    "tiempo": float(coincidencia.group(1)),
                    "tokens": int(coincidencia.group(2)),
                    "velocidad": float(coincidencia.group(3)),
                }

            coincidencia = PATRONES["tiempo_total"].search(linea)
            if coincidencia:
                self.estado["tiempo_total_ms"] = float(coincidencia.group(1))
                self.estado["tokens_totales"] = int(coincidencia.group(2))
                self.estado["ultimo_total"] = {
                    "tiempo": float(coincidencia.group(1)),
                    "tokens": int(coincidencia.group(2)),
                }

            if PATRONES["chat_ejecutando"].search(linea):
                coincidencia_chat = PATRONES["chat_ejecutando"].search(linea)
                if coincidencia_chat:
                    self.estado["chat_ejecutandose"] = True
                    self.estado["mensajes_chat"] = int(coincidencia_chat.group(1))

            if PATRONES["streaming_inicio"].search(linea):
                self.estado["transmitiendo"] = True
            if PATRONES["streaming_fin"].search(linea):
                self.estado["transmitiendo"] = False
                self.estado["chat_ejecutandose"] = False

            coincidencia = PATRONES["peticion_recibida"].search(linea)
            if coincidencia:
                self.estado["ultima_peticion"] = self.marca_tiempo
                self.estado["endpoint_ultima_peticion"] = f"{coincidencia.group(1)} {coincidencia.group(2)}"

            if PATRONES["error"].search(linea):
                linea_limpia = re.sub(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[.*?\]\s*", "", linea).strip()
                if linea_limpia and len(linea_limpia) > 10:
                    self.errores_recientes.append((self.marca_tiempo, linea_limpia[:90]))

        self.estado["errores"] = self.errores_recientes[-5:]
        self.estado["lineas_log"] += len(lineas)
        return self.estado


# Patrones de expresiones regulares para extraer información de los logs
PATRONES = {
    "servidor_iniciado": re.compile(r"Server started"),
    "servidor_detenido": re.compile(r"Server stopped"),
    "servidor_escuchando": re.compile(r"listening on port (\d+)"),
    "modelo_cargando": re.compile(r"load_model: loading model '([^']+)'"),
    "modelo_cargado": re.compile(r"model loaded"),
    "modelo_slots": re.compile(r"n_slots = (\d+), n_ctx_slot = (\d+)"),
    "progreso_prompt": re.compile(r"Prompt processing progress: ([\d.]+)%"),
    "velocidad_procesamiento_prompt": re.compile(
        r"prompt processing, n_tokens =\s*(\d+), progress = [\d.]+, t =\s*([\d.]+) s / ([\d.]+) tokens per second"
    ),
    "evaluacion_prompt": re.compile(
        r"prompt eval time =\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second"
    ),
    "evaluacion_generacion": re.compile(
        r"(?<!prompt )eval time =\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second"
    ),
    "tiempo_total": re.compile(r"total time =\s*([\d.]+) ms /\s*(\d+) tokens"),
    "chat_ejecutando": re.compile(r"Running chat completion on conversation with (\d+) messages"),
    "streaming_inicio": re.compile(r"Streaming response"),
    "streaming_fin": re.compile(r"Finished streaming response"),
    "peticion_recibida": re.compile(r"Received request: (GET|POST) to (\S+)"),
    "error": re.compile(r"ERROR|error|failed", re.IGNORECASE),
    "archivo_modelo": re.compile(r"loading model '([^']+)'"),
}


def obtener_theme(nombre: str = None) -> dict:
    """
    Obtiene la paleta de colores del theme especificado.

    Args:
        nombre: Nombre del theme. Si es None, usa THEME_ACTUAL.

    Returns:
        dict: Diccionario con los colores del theme.
    """
    nombre = nombre or THEME_ACTUAL
    return THEMES.get(nombre, THEMES["dracula"])


# =============================================================================
# FUNCIONES DE BÚSQUEDA Y PARSING
# =============================================================================

def buscar_ultimo_log(ruta_base: Path | None = None) -> Path:
    """
    Busca y devuelve la ruta al archivo de log más reciente.

    Prioriza el log del día actual. Si no existe, busca en los últimos
    12 meses en orden cronológico inverso.

    Args:
        ruta_base: Directorio raíz donde buscar los logs.
                   Si es None, se autodetecta (ver detectar_ruta_base()).

    Returns:
        Path: Ruta al archivo de log más reciente encontrado.
              Si no se encuentra ningún log, devuelve una ruta por defecto
              para el día actual (que puede no existir).
    """
    if ruta_base is None:
        ruta_base = detectar_ruta_base()
    ruta_base = Path(ruta_base)
    ahora = datetime.now()

    # 1. Intentar encontrar log del día actual
    ruta_hoy = ruta_base / f"{ahora.year:04d}-{ahora.month:02d}"
    if ruta_hoy.exists():
        patron_hoy = f"{ahora.strftime('%Y-%m-%d')}*.log"
        logs_hoy = sorted(ruta_hoy.glob(patron_hoy), reverse=True)
        for log in logs_hoy:
            if log.exists() and log.stat().st_size > 0:
                return log

    # 2. Buscar en los últimos 12 meses
    meses_buscar = []
    for meses_atras in range(1, 13):
        anio = ahora.year
        mes = ahora.month - meses_atras
        while mes <= 0:
            mes += 12
            anio -= 1
        meses_buscar.append(f"{anio:04d}-{mes:02d}")

    for directorio_mes in meses_buscar:
        ruta_mes = ruta_base / directorio_mes
        if ruta_mes.exists():
            logs = sorted(ruta_mes.glob("*.log"), reverse=True)
            for log in logs:
                if log.exists() and log.stat().st_size > 0:
                    return log

    # 3. Si no se encontró nada, devolver ruta por defecto para hoy
    return ruta_base / f"{ahora.year:04d}-{ahora.month:02d}" / f"{ahora.strftime('%Y-%m-%d')}.1.log"


def parsear_cola_log(ruta_archivo: Path, max_lineas: int = 1500) -> dict:
    """
    Analiza un archivo de log y extrae el estado actual del servidor.

    Lee el archivo completo para logs pequeños, o combina las primeras
    y últimas líneas para archivos grandes.

    Args:
        ruta_archivo: Ruta al archivo de log a analizar.
        max_lineas: Número máximo de líneas a procesar (por defecto 1500).

    Returns:
        dict: Diccionario con el estado extraído del servidor.
    """
    estado = {
        "estado_servidor": "Desconocido",
        "puerto_servidor": "-",
        "nombre_modelo": "-",
        "archivo_modelo": "-",
        "modelo_cargado": False,
        "num_slots": "-",
        "contexto_por_slot": "-",
        "progreso_prompt": 0.0,
        "progreso_prompt_activo": False,
        "tokens_prompt": 0,
        "velocidad_prompt": 0.0,
        "tiempo_eval_prompt": 0.0,
        "tokens_eval_prompt": 0,
        "velocidad_eval_prompt": 0.0,
        "tiempo_eval_generacion": 0.0,
        "tokens_eval_generacion": 0,
        "velocidad_eval_generacion": 0.0,
        "tiempo_total_ms": 0.0,
        "tokens_totales": 0,
        "chat_ejecutandose": False,
        "mensajes_chat": 0,
        "transmitiendo": False,
        "ultima_peticion": "-",
        "hora_ultima_peticion": "-",
        "endpoint_ultima_peticion": "-",
        "ultima_eval_prompt": None,
        "ultima_eval_generacion": None,
        "ultimo_total": None,
        "errores": [],
        "archivo_log": str(ruta_archivo),
        "lineas_log": 0,
        "error_lectura": None,
    }

    try:
        with open(ruta_archivo, "r", errors="replace") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        estado["error_lectura"] = f"Archivo de log no encontrado: {ruta_archivo}"
        return estado

    if len(lineas) <= max_lineas:
        lineas_combinadas = lineas
    else:
        cabecera = lineas[:400]
        cola = lineas[-max_lineas:]
        lineas_combinadas = cabecera + cola

    estado["lineas_log"] = len(lineas)

    errores_recientes = []
    marca_tiempo = "-"

    for linea in lineas_combinadas:
        coincidencia_ts = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", linea)
        if coincidencia_ts:
            marca_tiempo = coincidencia_ts.group(1)

        coincidencia = PATRONES["servidor_escuchando"].search(linea)
        if coincidencia:
            estado["puerto_servidor"] = coincidencia.group(1)
            estado["estado_servidor"] = "Activo"

        if PATRONES["servidor_iniciado"].search(linea):
            estado["estado_servidor"] = "Activo"
        if PATRONES["servidor_detenido"].search(linea):
            estado["estado_servidor"] = "Detenido"

        coincidencia = PATRONES["modelo_cargando"].search(linea)
        if coincidencia:
            estado["archivo_modelo"] = Path(coincidencia.group(1)).name
            ruta_completa = coincidencia.group(1)
            partes = ruta_completa.split("/")
            if len(partes) >= 3:
                estado["nombre_modelo"] = "/".join(partes[-2:])
            else:
                estado["nombre_modelo"] = Path(ruta_completa).name

        if PATRONES["modelo_cargado"].search(linea):
            estado["modelo_cargado"] = True

        coincidencia = PATRONES["modelo_slots"].search(linea)
        if coincidencia:
            estado["num_slots"] = coincidencia.group(1)
            estado["contexto_por_slot"] = coincidencia.group(2)

        coincidencia = PATRONES["progreso_prompt"].search(linea)
        if coincidencia:
            porcentaje = float(coincidencia.group(1))
            estado["progreso_prompt"] = porcentaje
            estado["progreso_prompt_activo"] = porcentaje < 100.0

        coincidencia = PATRONES["velocidad_procesamiento_prompt"].search(linea)
        if coincidencia:
            estado["tokens_prompt"] = int(coincidencia.group(1))
            estado["velocidad_prompt"] = float(coincidencia.group(3))

        coincidencia = PATRONES["evaluacion_prompt"].search(linea)
        if coincidencia:
            estado["tiempo_eval_prompt"] = float(coincidencia.group(1))
            estado["tokens_eval_prompt"] = int(coincidencia.group(2))
            estado["velocidad_eval_prompt"] = float(coincidencia.group(3))
            estado["ultima_eval_prompt"] = {
                "tiempo": float(coincidencia.group(1)),
                "tokens": int(coincidencia.group(2)),
                "velocidad": float(coincidencia.group(3)),
            }

        coincidencia = PATRONES["evaluacion_generacion"].search(linea)
        if coincidencia:
            estado["tiempo_eval_generacion"] = float(coincidencia.group(1))
            estado["tokens_eval_generacion"] = int(coincidencia.group(2))
            estado["velocidad_eval_generacion"] = float(coincidencia.group(3))
            estado["ultima_eval_generacion"] = {
                "tiempo": float(coincidencia.group(1)),
                "tokens": int(coincidencia.group(2)),
                "velocidad": float(coincidencia.group(3)),
            }

        coincidencia = PATRONES["tiempo_total"].search(linea)
        if coincidencia:
            estado["tiempo_total_ms"] = float(coincidencia.group(1))
            estado["tokens_totales"] = int(coincidencia.group(2))
            estado["ultimo_total"] = {
                "tiempo": float(coincidencia.group(1)),
                "tokens": int(coincidencia.group(2)),
            }

        if PATRONES["chat_ejecutando"].search(linea):
            coincidencia_chat = PATRONES["chat_ejecutando"].search(linea)
            if coincidencia_chat:
                estado["chat_ejecutandose"] = True
                estado["mensajes_chat"] = int(coincidencia_chat.group(1))

        if PATRONES["streaming_inicio"].search(linea):
            estado["transmitiendo"] = True
        if PATRONES["streaming_fin"].search(linea):
            estado["transmitiendo"] = False
            estado["chat_ejecutandose"] = False

        coincidencia = PATRONES["peticion_recibida"].search(linea)
        if coincidencia:
            estado["ultima_peticion"] = marca_tiempo
            estado["endpoint_ultima_peticion"] = f"{coincidencia.group(1)} {coincidencia.group(2)}"

        if PATRONES["error"].search(linea):
            linea_limpia = re.sub(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[.*?\]\s*", "", linea).strip()
            if linea_limpia and len(linea_limpia) > 10:
                errores_recientes.append((marca_tiempo, linea_limpia[:90]))

    estado["errores"] = errores_recientes[-5:]
    return estado


# =============================================================================
# FUNCIONES DE CONSTRUCCIÓN DE LA INTERFAZ
# =============================================================================

def construir_panel(estado: dict, theme: dict = None) -> Layout:
    """
    Construye el panel de control Rich a partir del estado parseado.

    Crea una interfaz visual con secciones para:
    - Información del servidor y modelo
    - Procesamiento de prompt y generación
    - Última petición completada y errores recientes

    Args:
        estado: Diccionario con el estado del servidor.
        theme: Diccionario de colores del theme a usar.

    Returns:
        Layout: Disposición Rich con todos los paneles.
    """
    if theme is None:
        theme = obtener_theme()

    layout = Layout()

    # Cabecera del monitor
    linea_cabecera = Text()
    linea_cabecera.append("  LMStudio Monitor", style=f"bold {theme['primario']}")
    linea_cabecera.append(f"  {SIMBOLOS['separador']}  ", style=theme['apagado'])
    linea_cabecera.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style=theme['apagado'])
    linea_cabecera.append(f"  {SIMBOLOS['separador']}  ", style=theme['apagado'])
    linea_cabecera.append(f"{estado.get('archivo_log', '')}", style=f"italic {theme['apagado']}")
    linea_cabecera.append(f"  {SIMBOLOS['titulo']} [q] Salir", style=f"bold {theme['error']}")

    layout.split_column(
        Layout(linea_cabecera, size=3),
        Layout(name="superior", size=8),
        Layout(name="medio", size=7),
        Layout(name="inferior"),
    )

    # --- Fila superior: Servidor + Modelo ---
    tabla_servidor = Table(show_header=False, box=None, padding=(0, 1))
    tabla_servidor.add_column("Clave", style=f"bold {theme['secundario']}", width=14)
    tabla_servidor.add_column("Valor", style=theme['texto'])

    estado_servidor = estado["estado_servidor"]
    if estado_servidor == "Activo":
        estilo_estado = f"bold {theme['estado_activo']}"
        icono_estado = SIMBOLOS["activo"]
    elif estado_servidor == "Detenido":
        estilo_estado = f"bold {theme['estado_detenido']}"
        icono_estado = SIMBOLOS["detenido"]
    else:
        estilo_estado = f"bold {theme['estado_advertencia']}"
        icono_estado = SIMBOLOS["advertencia"]

    tabla_servidor.add_row("Estado", Text(f"{icono_estado} {estado_servidor}", style=estilo_estado))
    tabla_servidor.add_row("Puerto", estado["puerto_servidor"])
    tabla_servidor.add_row("Última petición", estado["ultima_peticion"])
    tabla_servidor.add_row("Endpoint", estado["endpoint_ultima_peticion"])

    tabla_modelo = Table(show_header=False, box=None, padding=(0, 1))
    tabla_modelo.add_column("Clave", style=f"bold {theme['secundario']}", width=14)
    tabla_modelo.add_column("Valor", style=theme['texto'])

    nombre_modelo = estado["nombre_modelo"]
    if estado["modelo_cargado"]:
        estilo_modelo = f"bold {theme['estado_activo']}"
    else:
        estilo_modelo = f"bold {theme['estado_advertencia']}"

    tabla_modelo.add_row("Modelo", Text(nombre_modelo, style=estilo_modelo))
    tabla_modelo.add_row("Archivo", estado["archivo_modelo"])
    tabla_modelo.add_row("Slots / Ctx", f"{estado['num_slots']} slots  │  {estado['contexto_por_slot']} tokens")

    layout["superior"].split_row(
        Layout(Panel(tabla_servidor, title=f"[bold {theme['primario']}]Servidor[/bold {theme['primario']}]", border_style=theme['borde_panel']), ratio=1),
        Layout(Panel(tabla_modelo, title=f"[bold {theme['primario']}]Modelo[/bold {theme['primario']}]", border_style=theme['borde_panel']), ratio=1),
    )

    # --- Fila medio: Progreso de prompt + Generación ---
    lineas_prompt = Table(show_header=False, box=None, padding=(0, 1))
    lineas_prompt.add_column("Clave", style=f"bold {theme['secundario']}", width=18)
    lineas_prompt.add_column("Valor", style=theme['texto'])

    if estado["progreso_prompt_activo"]:
        porcentaje = estado["progreso_prompt"]
        ancho_barra = 30
        relleno = int(ancho_barra * porcentaje / 100)
        barra = f"{SIMBOLOS['barra_llena'] * relleno}{SIMBOLOS['barra_vacia'] * (ancho_barra - relleno)}"
        lineas_prompt.add_row("Progreso", Text(f"[{barra}] {porcentaje:.1f}%", style=f"bold {theme['terciario']}"))
        lineas_prompt.add_row("Tokens procesados", str(estado["tokens_prompt"]))
        lineas_prompt.add_row("Velocidad", f"{estado['velocidad_prompt']:.2f} tok/s")
    elif estado["tokens_eval_prompt"] > 0:
        lineas_prompt.add_row("Prompt eval", f"{estado['tokens_eval_prompt']} tokens")
        lineas_prompt.add_row("Tiempo", f"{estado['tiempo_eval_prompt']:.2f} ms")
        lineas_prompt.add_row("Velocidad", f"{estado['velocidad_eval_prompt']:.2f} tok/s")
    else:
        lineas_prompt.add_row("Estado", Text("Sin procesamiento activo", style=theme['apagado']))

    lineas_generacion = Table(show_header=False, box=None, padding=(0, 1))
    lineas_generacion.add_column("Clave", style=f"bold {theme['secundario']}", width=18)
    lineas_generacion.add_column("Valor", style=theme['texto'])

    if estado["tokens_eval_generacion"] > 0:
        lineas_generacion.add_row("Tokens generados", str(estado["tokens_eval_generacion"]))
        lineas_generacion.add_row("Tiempo", f"{estado['tiempo_eval_generacion']:.2f} ms")
        lineas_generacion.add_row("Velocidad", f"{estado['velocidad_eval_generacion']:.2f} tok/s")
    else:
        lineas_generacion.add_row("Estado", Text("Sin generación activa", style=theme['apagado']))

    if estado["transmitiendo"]:
        insignia_streaming = Text(f"  {SIMBOLOS['streaming']} STREAMING ACTIVO  ", style=f"bold {theme['texto']} on {theme['estado_activo']}")
    else:
        insignia_streaming = Text("  Inactivo  ", style=theme['apagado'])

    titulo_medio = Text()
    titulo_medio.append(f"Generación  ", style=theme['texto'])
    titulo_medio.append(insignia_streaming)

    layout["medio"].split_row(
        Layout(Panel(lineas_prompt, title=f"[bold {theme['primario']}]Procesamiento de Prompt[/bold {theme['primario']}]", border_style=theme['borde_panel']), ratio=1),
        Layout(Panel(lineas_generacion, title=titulo_medio, border_style=theme['borde_panel']), ratio=1),
    )

    # --- Fila inferior: Última completada + Errores ---
    ultima_completada = Table(show_header=False, box=None, padding=(0, 1))
    ultima_completada.add_column("Clave", style=f"bold {theme['secundario']}", width=22)
    ultima_completada.add_column("Valor", style=theme['texto'])

    if estado["ultima_eval_prompt"]:
        eval_prompt = estado["ultima_eval_prompt"]
        ultima_completada.add_row("Prompt (último)", f"{eval_prompt['tokens']} tokens @ {eval_prompt['velocidad']:.2f} tok/s")
    if estado["ultima_eval_generacion"]:
        eval_generacion = estado["ultima_eval_generacion"]
        ultima_completada.add_row("Generación (última)", f"{eval_generacion['tokens']} tokens @ {eval_generacion['velocidad']:.2f} tok/s")
    if estado["ultimo_total"]:
        total = estado["ultimo_total"]
        ultima_completada.add_row("Total", f"{total['tokens']} tokens en {total['tiempo']:.2f} ms")
    if not estado["ultima_eval_prompt"] and not estado["ultima_eval_generacion"]:
        ultima_completada.add_row("Estado", Text("Aún no hay peticiones completadas", style=theme['apagado']))

    tabla_errores = Table(show_header=False, box=None, padding=(0, 1), expand=True)
    tabla_errores.add_column("Hora", style=theme['apagado'], width=12)
    tabla_errores.add_column("Error", style=f"bold {theme['error']}")

    for marca_ts, mensaje in estado.get("errores", []):
        ts_corto = marca_ts.split(" ")[1] if " " in marca_ts else marca_ts
        tabla_errores.add_row(ts_corto, mensaje)

    if not estado.get("errores"):
        tabla_errores.add_row("-", Text("Sin errores recientes", style=theme['apagado']))

    titulo_errores = Text()
    titulo_errores.append(f"{SIMBOLOS['error']} Errores Recientes", style=f"bold {theme['error']}")

    layout["inferior"].split_row(
        Layout(Panel(ultima_completada, title=f"[bold {theme['primario']}]◆ Última Petición Completada[/bold {theme['primario']}]", border_style=theme['borde_panel']), ratio=1),
        Layout(Panel(tabla_errores, title=titulo_errores, border_style=theme['error']), ratio=1),
    )

    return layout


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def principal():
    """
    Función principal del monitor.

    Gestiona la línea de comandos, inicializa la consola Rich y ejecuta
    el bucle principal de actualización del panel de control.
    """
    consola = Console()

    # Mostrar ayuda si se solicita
    if "--help" in sys.argv or "-h" in sys.argv:
        consola.print("[bold]LMStudio Monitor[/bold] — Panel de control TUI en tiempo real de logs de LMStudio")
        consola.print()
        consola.print("Uso: python3 lmstudio-monitor.py [opciones]")
        consola.print()
        consola.print("Opciones:")
        consola.print("  --help, -h         Mostrar esta ayuda")
        consola.print("  --interval N       Intervalo de actualización en segundos (default: 2)")
        consola.print("  --file PATH        Archivo de log específico a monitorear")
        consola.print("  --platform PLAT    Plataforma de logs: auto (default), linux o windows")
        consola.print("                     linux   -> ~/.lmstudio/server-logs")
        consola.print("                     windows -> ~/.lmstudio/apps/bionic/server-logs")
        consola.print("                                (p. ej. C:\\Users\\<usuario>\\.lmstudio\\apps\\bionic\\server-logs)")
        consola.print("  --logs-dir DIR     Directorio raíz de logs personalizado (tiene prioridad")
        consola.print("                     sobre --platform; útil para una ruta nueva cualquiera)")
        consola.print(f"  --theme THEME      Theme de colores (disponibles: {', '.join(THEMES.keys())})")
        consola.print()
        consola.print("Detección automática (--platform auto, por defecto):")
        consola.print("  Elige la ruta existente; si existen ambas, la del *.log más reciente;")
        consola.print("  si no existe ninguna, usa la nativa del SO actual.")
        consola.print()
        consola.print("Ejemplos:")
        consola.print("  python3 lmstudio-monitor.py                              # autodetectar")
        consola.print("  python3 lmstudio-monitor.py --platform windows           # forzar ruta Windows")
        consola.print("  python3 lmstudio-monitor.py --platform linux             # forzar ruta Linux")
        consola.print("  python3 lmstudio-monitor.py --logs-dir /ruta/nueva/logs # ruta personalizada")
        consola.print()
        consola.print(f"  Theme por defecto: {THEME_ACTUAL}")
        sys.exit(0)

    def _obtener_valor(*nombres):
        for i, arg in enumerate(sys.argv):
            if arg in nombres and i + 1 < len(sys.argv):
                return sys.argv[i + 1]
        return None

    # Parsear argumentos de línea de comandos
    intervalo = 2
    valor_intervalo = _obtener_valor("--interval")
    if valor_intervalo is not None:
        intervalo = float(valor_intervalo)

    valor_file = _obtener_valor("--file")
    archivo_fijo = Path(valor_file) if valor_file else None

    plataforma = _obtener_valor("--platform", "--os") or "auto"
    if plataforma.lower() not in ("auto", "linux", "windows", "win"):
        consola.print(f"[bold red]Error:[/bold red] Plataforma '{plataforma}' no válida.")
        consola.print("Valores válidos: auto, linux, windows")
        sys.exit(1)

    valor_logs_dir = _obtener_valor("--logs-dir", "--log-dir", "--ruta", "--path")
    if valor_logs_dir:
        ruta_logs = Path(valor_logs_dir)
        if not ruta_logs.exists():
            consola.print(f"[bold red]Error:[/bold red] Directorio '{ruta_logs}' no existe.")
            sys.exit(1)
    else:
        ruta_logs = resolver_ruta_base(plataforma)

    theme_nombre = THEME_ACTUAL
    for i, arg in enumerate(sys.argv):
        if arg == "--theme" and i + 1 < len(sys.argv):
            theme_solicitado = sys.argv[i + 1].lower()
            if theme_solicitado in THEMES:
                theme_nombre = theme_solicitado
            else:
                consola.print(f"[bold red]Error:[/bold red] Theme '{theme_solicitado}' no disponible.")
                consola.print(f"Themes disponibles: {', '.join(THEMES.keys())}")
                sys.exit(1)

    theme = obtener_theme(theme_nombre)
    archivo_log = archivo_fijo if archivo_fijo else buscar_ultimo_log(ruta_logs)

    consola.print(f"[bold {theme['terciario']}]Monitor iniciado[/bold {theme['terciario']}] — Theme: {theme_nombre} — Platform: {plataforma.lower()}")
    consola.print(f"[{theme['apagado']}]Logs: {ruta_logs}[/{theme['apagado']}]")
    consola.print(f"[{theme['apagado']}]Presiona q para salir[/{theme['apagado']}]")
    time.sleep(1)

    # Bucle principal de actualización
    lector = LectorLog()
    try:
        with Live(console=consola, refresh_per_second=1, screen=True) as en_vivo:
            while True:
                if not archivo_fijo:
                    nuevo_log = buscar_ultimo_log(ruta_logs)
                    if nuevo_log != archivo_log:
                        archivo_log = nuevo_log

                lineas_nuevas = lector.leer_nuevas_lineas(archivo_log)
                estado = lector.actualizar_estado(lineas_nuevas)
                if estado.get("error_lectura"):
                    panel = Panel(
                        f"[bold red]{estado['error_lectura']}[/bold red]\n\n"
                        f"[{theme['apagado']}]Esperando a que el archivo de log esté disponible...[/{theme['apagado']}]",
                        title=f"[bold {theme['primario']}]LMStudio Monitor[/bold {theme['primario']}]",
                        border_style=theme['error']
                    )
                else:
                    panel = construir_panel(estado, theme)
                en_vivo.update(panel)
                time.sleep(intervalo)
    except KeyboardInterrupt:
        pass

    consola.print(f"\n[bold {theme['primario']}]Monitor detenido.[/bold {theme['primario']}]")


if __name__ == "__main__":
    principal()
