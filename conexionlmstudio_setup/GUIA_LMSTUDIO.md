# Configuracion de OpenCode con LM Studio

Guia para conectar OpenCode con modelos locales via LM Studio.

## Requisitos Previos

1. LM Studio instalado en el servidor (`scacnet.cacsa.eu`)
2. Modelo **qwen3.5-9b** cargado en LM Studio
3. OpenCode instalado

## Paso 1: Verificar el Servidor LM Studio

El servidor corre en `http://scacnet.cacsa.eu:1234`. Para verificar:

```bash
curl http://scacnet.cacsa.eu:1234/v1/models
```

Respuesta esperada:

```json
{
  "data": [
    { "id": "qwen3.5-9b", "object": "model" },
    { "id": "text-embedding-nomic-embed-text-v1.5", "object": "model" }
  ]
}
```

> **Nota**: `text-embedding-nomic-embed-text-v1.5` es un modelo de embeddings, no de chat. No se incluye en la configuracion de OpenCode.

## Paso 2: Configurar `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://scacnet.cacsa.eu:1234/v1",
        "apiKey": "lm-studio",
        "timeout": 300000
      },
      "models": {
        "qwen3.5-9b": {
          "name": "Qwen3.5-9b (local)",
          "reasoning": true,
          "interleaved": {
            "field": "reasoning_content"
          },
          "limit": {
            "context": 50573,
            "output": 25286
          }
        }
      }
    }
  },
  "model": "lmstudio/qwen3.5-9b"
}
```

### Detalles de la configuracion

| Campo | Valor | Descripcion |
|-------|-------|-------------|
| `baseURL` | `http://scacnet.cacsa.eu:1234/v1` | URL del servidor LM Studio |
| `apiKey` | `lm-studio` | Placeholder (LM Studio no requiere API key) |
| `timeout` | `300000` | Timeout de 5 minutos para carga inicial del modelo |
| `reasoning` | `true` | Habilita el modo razonamiento del modelo |
| `interleaved.field` | `reasoning_content` | Muestra el chain-of-thought intercalado |
| `limit.context` | `50573` | Contexto maximo configurado en LM Studio |
| `limit.output` | `25286` | Tokens maximos de salida |

### Formato `proveedor/modelo`

El campo `"model": "lmstudio/qwen3.5-9b"` usa el formato **`proveedor/modelo`**:
- **`lmstudio/`** → indica a OpenCode que proveedor usar (el definido como `"lmstudio": { ... }`)
- **`qwen3.5-9b`** → ID exacto del modelo dentro de LM Studio

## Paso 3: Ejecucion

Con LM Studio sirviendo y `opencode.json` en el directorio raiz, OpenCode enviara todos los prompts al modelo local.

## Monitoreo de Contexto

### API (por peticion)
Cada respuesta incluye objeto `usage`: `prompt_tokens`, `completion_tokens`, `total_tokens`.

### Interfaz LM Studio
En la pestana **Local Server** > **Server Logs** se ve el contexto usado en tiempo real:
`Context limit (ej. 1200 / 50573)`

## Optimizacion de Contexto

El modelo Qwen3.5-9B tiene **50.573 tokens de contexto**. Para aprovecharlo al maximo:

1. **Fragmentacion de Tareas**: Divide peticiones grandes en pasos atomicos.
2. **Planning Mode**: Usa el modo planificacion para tareas complejas (genera `task.md`).
3. **Reinicio de Sesion**: Si el modelo se vuelve lento o incoherente, abre una nueva sesion.
4. **Configuracion en LM Studio**: En el panel derecho del modelo, ajusta "Context Length". Para Qwen3.5-9B se recomienda `50573` segun VRAM disponible.

## Timeout

El provider tiene configurado `timeout: 300000` (5 minutos). Si una peticion excede ese tiempo, OpenCode la aborta. Esto evita que el agente quede colgado si LM Studio se congela.
