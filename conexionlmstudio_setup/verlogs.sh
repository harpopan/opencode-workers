#!/bin/bash
# verlogs.sh - Arranca el servidor de logs de LM Studio

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Configuracion
export LM_LOG_PORT="${LM_LOG_PORT:-1235}"

echo "=== LM Studio Log Server ==="
echo "Puerto: $LM_LOG_PORT"
echo ""

cd "$SCRIPT_DIR" || exit 1
python3 "$SCRIPT_DIR/servidorlogslmstudio.py"
