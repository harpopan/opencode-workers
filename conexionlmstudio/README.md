# OpenCode + LM Studio — Conexión Local

Configuración de **OpenCode** conectado a **LM Studio** para ejecutar modelos de lenguaje de forma local y privada.

## Requisitos

- LM Studio con servidor de API activo
- Modelo `google/gemma-4-e4b` cargado en LM Studio
- OpenCode instalado

## Configuración

Ver `opencode.json` (única fuente de verdad). La configuración apunta a:

- **Server**: `http://scacnet.cacsa.eu:1234/v1`
- **Modelo**: `google/gemma-4-e4b` (contexto 14096 tokens)
- **Timeout**: 120s
- **Reasoning**: activado (`reasoning_content`)

## Documentación

| Archivo | Propósito |
|---------|-----------|
| `opencode.json` | Configuración principal |
| `GUIA_LMSTUDIO.md` | Guía detallada de LM Studio |
| `AGENTS.md` | Instrucciones para el agente |
| `ESTRUCTURA_PROYECTO.md` | Estructura de archivos |
