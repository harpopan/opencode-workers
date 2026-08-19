# Configurador automático de opencode.jsonc para LMStudio
# Detecta modelos disponibles en LMStudio y configura opencode.jsonc

$LMSTUDIO_URL = if ($env:LMSTUDIO_URL) {
    $env:LMSTUDIO_URL
}
else {
    "http://localhost:1234"
}

$CONFIG_FILE = Join-Path (Get-Location) "opencode.jsonc"

Write-Host "=== Configurador OpenCode + LMStudio ==="
Write-Host ""

# ============================================================
# 1. Verificar conexión con LMStudio
# ============================================================

Write-Host "1. Verificando conexión con LMStudio en $LMSTUDIO_URL ..."

try {
    $ModelsResponse = Invoke-RestMethod `
        -Uri "$LMSTUDIO_URL/v1/models" `
        -Method Get `
        -ErrorAction Stop
}
catch {
    Write-Host "   [ERROR] No se pudo conectar a LMStudio" -ForegroundColor Red
    Write-Host "   Asegúrate de que LMStudio está corriendo en $LMSTUDIO_URL"
    Write-Host ""
    Write-Host "   Detalle: $($_.Exception.Message)"
    exit 1
}

# Intentar obtener información detallada de la API nativa de LMStudio
$NativeAPIURL = "$LMSTUDIO_URL/api/v1"
$NativeModelsResponse = $null
try {
    $NativeModelsResponse = Invoke-RestMethod `
        -Uri "$NativeAPIURL/models" `
        -Method Get `
        -ErrorAction Stop
}
catch {
    Write-Host "   [WARN] No se pudo obtener información detallada de la API nativa" -ForegroundColor Yellow
    Write-Host "   Se usarán valores por defecto para context_length y max_tokens"
}

# ============================================================
# 2. Obtener modelos disponibles
# ============================================================

$Models = @(
    $ModelsResponse.data |
        Where-Object {
            $_.id -notlike "text-embedding*"
        } |
        ForEach-Object {
            $_.id
        }
)

if ($Models.Count -eq 0) {

    Write-Host "   [ERROR] No se encontraron modelos de chat disponibles" -ForegroundColor Red
    Write-Host "   Modelos en el servidor:"

    if ($ModelsResponse.data) {
        $ModelsResponse.data | ForEach-Object {
            Write-Host "     - $($_.id)"
        }
    }
    else {
        Write-Host "     (ninguno)"
    }

    exit 1
}

Write-Host "   [OK] Encontrados $($Models.Count) modelo(s) de chat:" -ForegroundColor Green

foreach ($Model in $Models) {
    Write-Host "     - $Model"
}

Write-Host ""

# ============================================================
# 3. Seleccionar modelo por defecto
# ============================================================

$DefaultModel = $Models[0]

Write-Host "2. Modelo por defecto: $DefaultModel"
Write-Host ""

# ============================================================
# 4. Construir configuración OpenCode
# ============================================================

Write-Host "3. Generando configuración en $CONFIG_FILE ..."

try {

    # Diccionario de modelos nativos para lookup rápido
    $NativeModelsDict = @{}
    if ($NativeModelsResponse -and $NativeModelsResponse.models) {
        foreach ($NativeModel in $NativeModelsResponse.models) {
            if ($NativeModel.key) {
                $NativeModelsDict[$NativeModel.key] = $NativeModel
            }
        }
    }

    # Valores por defecto para max_tokens
    $DefaultMaxTokens = 8192

    # Diccionario de modelos
    $ModelsDict = [ordered]@{}

    foreach ($Model in $Models) {

        $ModelName = ($Model -split "/")[-1]

        # Obtener información nativa si está disponible
        $NativeModel = $NativeModelsDict[$Model]
        $ContextLength = 32768  # valor por defecto
        $MaxTokens = $DefaultMaxTokens

        if ($NativeModel) {
            # Usar max_context_length del modelo nativo
            if ($NativeModel.max_context_length) {
                $ContextLength = $NativeModel.max_context_length
            }
            # Si hay instancias cargadas, usar context_length de la configuración
            if ($NativeModel.loaded_instances -and $NativeModel.loaded_instances.Count -gt 0) {
                $LoadedConfig = $NativeModel.loaded_instances[0].config
                if ($LoadedConfig -and $LoadedConfig.context_length) {
                    $ContextLength = $LoadedConfig.context_length
                }
            }
        }

        $ModelsDict[$Model] = [ordered]@{
            name = $ModelName
            limit = [ordered]@{
                context = $ContextLength
                output = $MaxTokens
            }
        }
    }

    # Configuración principal
    $Config = [ordered]@{
        '$schema' = "https://opencode.ai/config.json"

        provider = [ordered]@{
            lmstudio = [ordered]@{
                npm = "@ai-sdk/openai-compatible"
                name = "LM Studio (local)"

                options = [ordered]@{
                    baseURL = "$LMSTUDIO_URL/v1"
                }

                models = $ModelsDict
            }
        }

        model = "lmstudio/$DefaultModel"
    }

    # Convertir a JSON
    $Json = $Config | ConvertTo-Json -Depth 10

    # Guardar como UTF-8 sin BOM
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $CONFIG_FILE,
        $Json,
        $Utf8NoBom
    )
}
catch {

    Write-Host "   [ERROR] Error al generar el archivo" -ForegroundColor Red
    Write-Host "   Detalle: $($_.Exception.Message)"
    exit 1
}

Write-Host "   [OK] Configuración generada" -ForegroundColor Green
Write-Host ""

# ============================================================
# 5. Mostrar configuración generada
# ============================================================

Write-Host "4. Contenido del archivo:"
Write-Host "-------------------------------------"

Get-Content -Path $CONFIG_FILE

Write-Host ""
Write-Host "-------------------------------------"
Write-Host ""

Write-Host "[OK] Configuración completada!" -ForegroundColor Green
Write-Host "     Archivo: $CONFIG_FILE"
Write-Host "     Modelo por defecto: $DefaultModel"
Write-Host ""
Write-Host "Para cambiar de modelo en OpenCode, usa /models"
Write-Host ""