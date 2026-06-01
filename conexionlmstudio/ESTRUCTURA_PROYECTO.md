# Estructura de Archivos

## /conexionlmstudio/

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
├── opencode.json            # Configuracion principal (single source of truth)
└── tui.json                 # Tema de la interfaz de terminal
```

## Archivos Principales

### `opencode.json`
Configuracion principal. Define el provider LM Studio, el modelo `google/gemma-4-e4b`, timeout, razonamiento, y limites de contexto.

### `AGENTS.md`
Instrucciones especificas para que el agente opere correctamente con el modelo local (contexto limitado a 14096 tokens, lectura selectiva, puntos de control).

### `GUIA_LMSTUDIO.md`
Guia completa: requisitos, configuracion del servidor, campos del JSON, monitoreo de contexto y optimizacion.

### `README.md`
Documentacion general del proyecto con enlaces a los demas archivos.

### `tui.json`
Configura el tema visual de la terminal de OpenCode.
