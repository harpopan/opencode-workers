#!/bin/bash
# arrancar.sh - Selecciona modelo LM Studio y arranca OpenCode

LMSTUDIO_URL="http://scacnet.cacsa.eu:1234"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/opencode.json"
CONTEXT_FILE="$SCRIPT_DIR/.last_context"
DEFAULT_CONTEXT=4096

# Filtrar modelos duplicados con sufijo :N (ej: qwen3.5-9b:2)
FILTER_DUPLICATES=true

echo "=== OpenCode + LM Studio ==="
echo ""

# Obtener modelos cargados
RESPONSE=$(curl -s "$LMSTUDIO_URL/v1/models" 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$RESPONSE" ]; then
  echo "Error: No se pudo conectar a LM Studio en $LMSTUDIO_URL"
  exit 1
fi

# Extraer IDs de modelos
ALL_MODELS=($(echo "$RESPONSE" | grep '"id"' | sed 's/.*"id": *"\([^"]*\)".*/\1/'))

# Filtrar duplicados con sufijo :N si esta activado
if [ "$FILTER_DUPLICATES" = true ]; then
  MODELS=()
  for model in "${ALL_MODELS[@]}"; do
    BASE=$(echo "$model" | sed 's/:[0-9]*$//')
    # Solo agregar si no existe ya la version base
    FOUND=false
    for existing in "${MODELS[@]}"; do
      if [ "$existing" = "$BASE" ]; then
        FOUND=true
        break
      fi
    done
    if [ "$FOUND" = false ]; then
      MODELS+=("$BASE")
    fi
  done
else
  MODELS=("${ALL_MODELS[@]}")
fi

if [ ${#MODELS[@]} -eq 0 ]; then
  echo "Error: No se encontraron modelos en LM Studio"
  exit 1
fi

echo "Modelos cargados en LM Studio:"
echo ""
for i in "${!MODELS[@]}"; do
  echo "  $((i+1)). ${MODELS[$i]}"
done
echo ""

# Seleccionar modelo
read -p "Selecciona modelo (numero): " SELECTION

if [ -z "$SELECTION" ] || [ "$SELECTION" -lt 1 ] || [ "$SELECTION" -gt ${#MODELS[@]} ]; then
  echo "Error: Seleccion invalida"
  exit 1
fi

SELECTED_MODEL="${MODELS[$((SELECTION-1))]}"
echo "Modelo seleccionado: $SELECTED_MODEL"
echo ""

# Cargar ultimo contexto usado
if [ -f "$CONTEXT_FILE" ]; then
  LAST_CONTEXT=$(cat "$CONTEXT_FILE")
else
  LAST_CONTEXT=$DEFAULT_CONTEXT
fi

# Preguntar contexto
read -p "Longitud de contexto (default $LAST_CONTEXT): " CONTEXT_INPUT

if [ -z "$CONTEXT_INPUT" ]; then
  CONTEXT_LENGTH=$LAST_CONTEXT
else
  CONTEXT_LENGTH=$CONTEXT_INPUT
fi

# Guardar contexto para proximo uso
echo "$CONTEXT_LENGTH" > "$CONTEXT_FILE"

echo "Contexto: $CONTEXT_LENGTH tokens"
echo ""

# Calcular output maximo (mitad del contexto)
OUTPUT_LENGTH=$((CONTEXT_LENGTH / 2))

# Actualizar opencode.json
MODEL_NAME=$(echo "$SELECTED_MODEL" | sed 's/\// /g' | sed 's/^./\U&/')

python3 -c "
import json

with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

provider = config['provider']['lmstudio']
provider['models'] = {
    '$SELECTED_MODEL': {
        'name': '$MODEL_NAME (local)',
        'reasoning': True,
        'interleaved': {
            'field': 'reasoning_content'
        },
        'limit': {
            'context': $CONTEXT_LENGTH,
            'output': $OUTPUT_LENGTH
        }
    }
}

config['model'] = 'lmstudio/$SELECTED_MODEL'

with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"

echo "Configuracion actualizada en opencode.json"
echo ""
echo "Arrancando OpenCode con modelo: $SELECTED_MODEL"
echo "============================================"
echo ""

opencode
