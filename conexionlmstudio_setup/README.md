# OpenCode + LM Studio — Conexión Local

Configuración de **OpenCode** conectado a **LM Studio** para ejecutar modelos de lenguaje de forma local y privada.

## Requisitos

- LM Studio con servidor de API activo
- Modelo cargado en LM Studio
- OpenCode instalado

## Uso Rapido

### Arrancar OpenCode con modelo local
```bash
./arrancar.sh
```

### Ver logs de LM Studio en navegador
```bash
./verlogs.sh
```
Accede a `http://scacnet.cacsa.eu:1235`. Sirve la carpeta del script y todas sus subcarpetas como navegador de archivos.

El script consulta los modelos cargados en LM Studio, te permite seleccionar uno, configurar el contexto y arranca OpenCode.

## Configuración

Ver `opencode.json` (única fuente de verdad). La configuración apunta a:

- **Server**: `http://scacnet.cacsa.eu:1234/v1`
- **Modelo**: `qwen3.5-9b`
- **Timeout**: 300s (5 min, para carga inicial del modelo)
- **Reasoning**: activado (`reasoning_content`)
- **Contexto**: 50573 tokens

## Mejoras Pendientes

- Timeout configurable desde `arrancar.sh`
- Perfiles de modelo predefinidos (contexto, reasoning, etc.)
- Auto-deteccion de modelo activo sin seleccion manual

## Notas

- El script recuerda el ultimo valor de contexto usado (se guarda en `.last_context`)
- El timeout actual es 300s para cubrir la carga inicial del modelo en VRAM

## Documentación

| Archivo | Propósito |
|---------|-----------|
| `opencode.json` | Configuración principal |
| `arrancar.sh` | Script de selección de modelo y arranque |
| `GUIA_LMSTUDIO.md` | Guía detallada de LM Studio |
| `AGENTS.md` | Instrucciones para el agente |
| `ESTRUCTURA_PROYECTO.md` | Estructura de archivos |
