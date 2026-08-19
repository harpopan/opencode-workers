#!/bin/bash

# Configurador automático de opencode.jsonc para LMStudio
# Detecta modelos disponibles en LMStudio y configura opencode.jsonc

LMSTUDIO_URL="${LMSTUDIO_URL:-http://localhost:1234}"
CONFIG_FILE="$(pwd)/opencode.jsonc"

echo "=== Configurador OpenCode + LMStudio ==="
echo ""

# Verificar que LMStudio está corriendo
echo "1. Verificando conexión con LMStudio en $LMSTUDIO_URL ..."
MODELS_RESPONSE=$(curl -s "$LMSTUDIO_URL/v1/models" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$MODELS_RESPONSE" ]; then
    echo "   ✗ No se pudo conectar a LMStudio"
    echo "   Asegúrate de que LMStudio está corriendo en $LMSTUDIO_URL"
    exit 1
fi

# Intentar obtener información detallada de la API nativa de LMStudio
NATIVE_API_URL="$LMSTUDIO_URL/api/v1"
NATIVE_MODELS_RESPONSE=$(curl -s "$NATIVE_API_URL/models" 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$NATIVE_MODELS_RESPONSE" ]; then
    echo "   ⚠ No se pudo obtener información detallada de la API nativa"
    echo "   Se usarán valores por defecto para context_length y max_tokens"
fi

# Usar Python para parsear JSON y extraer modelos (excluir embedding models)
MODELS=$(python3 -c "
import json, sys
data = json.loads('''$MODELS_RESPONSE''')
models = [m['id'] for m in data.get('data', []) if not m['id'].startswith('text-embedding')]
for m in models:
    print(m)
" 2>/dev/null)

if [ -z "$MODELS" ]; then
    echo "   ✗ No se encontraron modelos de chat disponibles"
    echo "   Modelos en el servidor:"
    python3 -c "
import json
data = json.loads('''$MODELS_RESPONSE''')
for m in data.get('data', []):
    print('     -', m['id'])
" 2>/dev/null
    exit 1
fi

MODEL_COUNT=$(echo "$MODELS" | wc -l)
echo "   ✓ Encontrados $MODEL_COUNT modelo(s) de chat:"
echo "$MODELS" | while read -r model; do
    echo "     - $model"
done
echo ""

# Seleccionar modelo por defecto (el primero de la lista)
DEFAULT_MODEL=$(echo "$MODELS" | head -n1)
echo "2. Modelo por defecto: $DEFAULT_MODEL"
echo ""

# Generar el JSONC usando Python
echo "3. Generando configuración en $CONFIG_FILE ..."

python3 -c "
import json

models_raw = '''$MODELS'''
models = [m.strip() for m in models_raw.strip().split('\n') if m.strip()]
default_model = '$DEFAULT_MODEL'
base_url = '$LMSTUDIO_URL/v1'

# Parse native models response if available
native_raw = '''$NATIVE_MODELS_RESPONSE'''
native_models = {}
if native_raw.strip():
    try:
        native_data = json.loads(native_raw)
        for nm in native_data.get('models', []):
            if 'key' in nm:
                native_models[nm['key']] = nm
    except:
        pass

# Default max tokens
DEFAULT_MAX_TOKENS = 8192

# Formato correcto para LMStudio segun documentacion oficial
models_dict = {}
for m in models:
    model_name = m.split('/')[-1]
    context_length = 32768  # default
    max_tokens = DEFAULT_MAX_TOKENS

    if m in native_models:
        nm = native_models[m]
        # Use max_context_length if present
        if 'max_context_length' in nm:
            context_length = nm['max_context_length']
        # If there are loaded instances, use config.context_length
        loaded_instances = nm.get('loaded_instances', [])
        if loaded_instances and isinstance(loaded_instances, list):
            config = loaded_instances[0].get('config', {})
            if 'context_length' in config:
                context_length = config['context_length']
    
    models_dict[m] = {
        'name': model_name,
        'limit': {
            'context': context_length,
            'output': max_tokens
        }
    }

config = {
    '\$schema': 'https://opencode.ai/config.json',
    'provider': {
        'lmstudio': {
            'npm': '@ai-sdk/openai-compatible',
            'name': 'LM Studio (local)',
            'options': {
                'baseURL': base_url
            },
            'models': models_dict
        }
    },
    'model': f'lmstudio/{default_model}'
}

# Escribir con formato bonito
output = json.dumps(config, indent=2, ensure_ascii=False)
print(output)
" > "$CONFIG_FILE"

if [ $? -ne 0 ]; then
    echo "   ✗ Error al generar el archivo"
    exit 1
fi

echo "   ✓ Configuración generada"
echo ""

# Mostrar el archivo generado
echo "4. Contenido del archivo:"
echo "─────────────────────────────────────"
cat "$CONFIG_FILE"
echo ""
echo "─────────────────────────────────────"
echo ""
echo "✓ Configuración completada!"
echo "  Archivo: $CONFIG_FILE"
echo "  Modelo por defecto: $DEFAULT_MODEL"
echo ""
echo "Para cambiar de modelo en OpenCode, usa /models"
