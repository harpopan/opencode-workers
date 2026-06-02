# Estructura de Archivos

## /conexionlmstudio_setup/

```
├── .opencode/              # Configuracion interna de opencode
│   ├── package.json
│   ├── package-lock.json
│   ├── node_modules/
│   ├── themes/
│   │   └── lahermita.json
│   └── .gitignore
│
├── AGENTS.md               # Guia operativa para el agente
├── ESTRUCTURA_PROYECTO.md  # Este archivo
├── GUIA_LMSTUDIO.md        # Guia detallada de LM Studio
├── README.md               # Documentacion general
├── arrancar.sh               # Script de seleccion de modelo y arranque
├── servidorlogslmstudio.py   # Servidor web para logs (solo stdlib)
├── verlogs.sh                # Bash de arranque para servidor de logs
├── opencode.json             # Configuracion principal (single source of truth)
├── .gitignore                # Archivos de runtime (no trackear)
├── .last_context             # Persistencia del ultimo contexto usado
├── .last_reasoning           # Persistencia del ultimo valor de razonamiento
└── tui.json                  # Tema de la interfaz de terminal
```

## Archivos Principales

### `arrancar.sh`
Script interactivo que:
1. Consulta modelos cargados en LM Studio
2. Permite seleccionar uno
3. Pide longitud de contexto (default 4096)
4. Actualiza `opencode.json`
5. Arranca OpenCode

### `opencode.json`
Configuracion principal. Define el provider LM Studio, el modelo `qwen3.5-9b`, timeout, razonamiento, y limites de contexto.

### `AGENTS.md`
Instrucciones especificas para que el agente opere correctamente con el modelo local.

### `GUIA_LMSTUDIO.md`
Guia completa: requisitos, configuracion del servidor, campos del JSON, monitoreo de contexto y optimizacion.

### `README.md`
Documentacion general del proyecto con enlaces a los demas archivos.

### `tui.json`
Configura el tema visual de la terminal de OpenCode.
