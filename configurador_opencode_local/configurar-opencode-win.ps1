# Configurador automático de opencode.jsonc para LMStudio
# Permite elegir entre varios "proveedores" (máquinas de desarrollo local
# con LMStudio desplegado), detecta sus modelos disponibles y genera
# opencode.jsonc apuntando al que se seleccione.

[CmdletBinding()]
param(
    [Alias('p')]
    [string]$Proveedor,

    [Alias('u')]
    [string]$Url,

    [Alias('l')]
    [switch]$Listar,

    [Alias('h')]
    [switch]$Ayuda
)

# Forzar UTF-8 en consola (evita simbolos raros y acentos rotos en Windows PowerShell 5.1)
# Requiere ademas guardar este .ps1 como UTF-8 con BOM.
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
    if ($PSVersionTable.PSVersion.Major -lt 6) { chcp 65001 > $null }
} catch { }

$CONFIG_FILE = Join-Path (Get-Location) "opencode.jsonc"

# -------------------------------------------------------------
# Proveedores conocidos: "Nombre|URL_BASE"
# Edita esta lista para añadir tus máquinas de desarrollo.
# También se puede añadir/mantener en ~/.config/opencode/providers.conf
# (una línea "Nombre|URL" por proveedor); si existe, se añade a esta lista.
# -------------------------------------------------------------
$Proveedores = @(
    "Local|http://localhost:1234"
    "ScacNet|http://scacnet.cacsa.eu:1234"
    # "Portatil|http://192.168.1.60:1234"
)

$ArchivoProveedores = Join-Path $HOME ".config/opencode/providers.conf"
if (Test-Path $ArchivoProveedores) {
    Get-Content -Path $ArchivoProveedores | ForEach-Object {
        $linea = $_.Trim()
        if ($linea -and -not $linea.StartsWith("#")) {
            $Proveedores += $linea
        }
    }
}

# -------------------------------------------------------------
# Utilidades
# -------------------------------------------------------------

$NombreScript = [System.IO.Path]::GetFileName($PSCommandPath)

function MostrarUso {
    $Uso = @"
Uso: $NombreScript [opciones]

Opciones:
  -p, -Proveedor <N|nombre>   Selecciona el proveedor por índice o nombre
                              (evita el menú interactivo)
  -u, -Url <URL>              Usa una URL directa, ignorando la lista de proveedores
  -l, -Listar                 Lista los proveedores configurados y sale
  -h, -Ayuda                  Muestra esta ayuda

Variables de entorno:
  LMSTUDIO_URL   Si se define, tiene prioridad sobre todo lo anterior.

Proveedores se definen en el array `$Proveedores del script, y opcionalmente
en $ArchivoProveedores (una línea "Nombre|URL" por proveedor).
"@
    Write-Host $Uso
}

function ListarProveedores {
    Write-Host "Proveedores configurados:"
    $i = 1
    foreach ($p in $Proveedores) {
        $nombre = ($p -split "\|")[0]
        $url = ($p -split "\|")[1]
        Write-Host "  $i) $nombre  ($url)"
        $i++
    }
}

# Convierte "Nombre de máquina" en una clave válida para usar como
# nombre de provider en opencode.jsonc (minúsculas, sin espacios/símbolos)
function Slugificar {
    param([string]$Texto)
    $Resultado = $Texto.ToLowerInvariant()
    $Resultado = [regex]::Replace($Resultado, "[^a-z0-9]+", "-")
    $Resultado = $Resultado.Trim("-".ToCharArray())
    return $Resultado
}

if ($Ayuda) {
    MostrarUso
    exit 0
}

if ($Listar) {
    ListarProveedores
    exit 0
}

Write-Host "=== Configurador OpenCode + LMStudio ==="
Write-Host ""

# -------------------------------------------------------------
# 1. Selección de proveedor
# -------------------------------------------------------------
$NombreProveedor = ""

if ($env:LMSTUDIO_URL) {
    # La variable de entorno manda sobre todo lo demás (compatibilidad
    # con el comportamiento del script original)
    $URLSeleccionada = $env:LMSTUDIO_URL
    $NombreProveedor = "entorno"
    Write-Host "1. Usando LMSTUDIO_URL del entorno: $URLSeleccionada"
}
elseif ($Url) {
    $URLSeleccionada = $Url
    $NombreProveedor = "manual"
    Write-Host "1. Usando URL indicada por parámetro: $URLSeleccionada"
}
elseif ($Proveedores.Count -eq 1) {
    # Solo hay un proveedor definido: no tiene sentido preguntar
    $NombreProveedor = ($Proveedores[0] -split "\|")[0]
    $URLSeleccionada = ($Proveedores[0] -split "\|")[1]
    Write-Host "1. Único proveedor configurado: $NombreProveedor ($URLSeleccionada)"
}
else {
    if ($Proveedor) {
        # Selección no interactiva por índice o por nombre
        $Elegido = $null
        if ($Proveedor -match "^\d+$" `
            -and [int]$Proveedor -ge 1 `
            -and [int]$Proveedor -le $Proveedores.Count) {
            $Elegido = $Proveedores[([int]$Proveedor - 1)]
        }
        else {
            foreach ($p in $Proveedores) {
                if (($p -split "\|")[0] -eq $Proveedor) {
                    $Elegido = $p
                    break
                }
            }
        }
        if (-not $Elegido) {
            Write-Host "[ERROR] Proveedor '$Proveedor' no encontrado." -ForegroundColor Red
            ListarProveedores
            exit 1
        }
        $NombreProveedor = ($Elegido -split "\|")[0]
        $URLSeleccionada = ($Elegido -split "\|")[1]
        Write-Host "1. Proveedor seleccionado: $NombreProveedor ($URLSeleccionada)"
    }
    else {
        # Menú interactivo
        Write-Host "1. ¿A qué máquina de desarrollo quieres conectarte?"
        Write-Host ""
        $i = 1
        foreach ($p in $Proveedores) {
            Write-Host "   $i) $(($p -split '\|')[0])  ($(($p -split '\|')[1]))"
            $i++
        }
        Write-Host ""
        $Opcion = Read-Host "Elige un número [1-$($Proveedores.Count)]"

        if ($Opcion -notmatch "^\d+$" `
            -or [int]$Opcion -lt 1 `
            -or [int]$Opcion -gt $Proveedores.Count) {
            Write-Host "[ERROR] Opción inválida." -ForegroundColor Red
            exit 1
        }

        $Elegido = $Proveedores[([int]$Opcion - 1)]
        $NombreProveedor = ($Elegido -split "\|")[0]
        $URLSeleccionada = ($Elegido -split "\|")[1]
    }
}

$LMSTUDIO_URL = $URLSeleccionada
$ClaveProveedor = Slugificar $NombreProveedor
if (-not $ClaveProveedor) {
    $ClaveProveedor = "lmstudio"
}
Write-Host ""

# -------------------------------------------------------------
# 2. Verificar conexión con LMStudio
# -------------------------------------------------------------
Write-Host "2. Verificando conexión con LMStudio en $LMSTUDIO_URL ..."

try {
    $ModelsResponse = Invoke-RestMethod `
        -Uri "$LMSTUDIO_URL/v1/models" `
        -Method Get `
        -TimeoutSec 5 `
        -ErrorAction Stop
}
catch {
    Write-Host "   [ERROR] No se pudo conectar a LMStudio en $LMSTUDIO_URL" -ForegroundColor Red
    Write-Host "   Comprueba que está corriendo y accesible desde esta máquina."
    Write-Host ""
    Write-Host "   Detalle: $($_.Exception.Message)"
    exit 1
}

# Intentar obtener información detallada de la API nativa de LMStudio
# (no todas las versiones la exponen, así que un fallo aquí no es fatal)
$NativeAPIURL = "$LMSTUDIO_URL/api/v1"
$NativeModelsResponse = $null
try {
    $NativeModelsResponse = Invoke-RestMethod `
        -Uri "$NativeAPIURL/models" `
        -Method Get `
        -TimeoutSec 5 `
        -ErrorAction Stop
}
catch {
    Write-Host "   [WARN] No se pudo obtener información detallada de la API nativa" -ForegroundColor Yellow
    Write-Host "   Se usarán valores por defecto para context_length y max_tokens"
}

Write-Host "   [OK] Conectado" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------------
# 3. Obtener modelos de chat disponibles (se excluyen embeddings)
# -------------------------------------------------------------

$Models = @(
    $ModelsResponse.data |
        Where-Object {
            $_.id -notmatch "embed"
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

Write-Host "3. Encontrados $($Models.Count) modelo(s) de chat en '$NombreProveedor':"

foreach ($Model in $Models) {
    Write-Host "     - $Model"
}

Write-Host ""

# Seleccionar modelo por defecto (el primero de la lista)
$DefaultModel = $Models[0]

Write-Host "4. Modelo por defecto: $DefaultModel"
Write-Host ""

# -------------------------------------------------------------
# 4. Generar el JSONC
# -------------------------------------------------------------
Write-Host "5. Generando configuración en $CONFIG_FILE ..."

if (Test-Path $CONFIG_FILE) {
    Copy-Item -Path $CONFIG_FILE -Destination "$CONFIG_FILE.bak" -Force
    Write-Host "   (se guardó una copia del archivo anterior en $CONFIG_FILE.bak)"
}

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

    # Valores por defecto
    $DefaultMaxTokens = 8192
    $DefaultContext = 32768

    # Diccionario de modelos
    $ModelsDict = [ordered]@{}

    foreach ($Model in $Models) {

        $ModelName = ($Model -split "/")[-1]

        # Obtener información nativa si está disponible
        $NativeModel = $NativeModelsDict[$Model]
        $ContextLength = $DefaultContext
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

    $URLBase = $LMSTUDIO_URL.TrimEnd("/") + "/v1"

    # Bloque de proveedor (la clave es dinámica, se asigna tras crear el objeto)
    $ProveedorConfig = [ordered]@{}
    $ProveedorConfig[$ClaveProveedor] = [ordered]@{
        npm = "@ai-sdk/openai-compatible"
        name = "LM Studio ($NombreProveedor)"
        options = [ordered]@{
            baseURL = $URLBase
        }
        models = $ModelsDict
    }

    # Configuración principal
    $Config = [ordered]@{
        '$schema' = "https://opencode.ai/config.json"
        provider = $ProveedorConfig
        model = "$ClaveProveedor/$DefaultModel"
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

# -------------------------------------------------------------
# 5. Resumen
# -------------------------------------------------------------
Write-Host "6. Contenido del archivo:"
Write-Host "-------------------------------------"

Get-Content -Path $CONFIG_FILE

Write-Host "-------------------------------------"
Write-Host ""

Write-Host "[OK] Configuración completada!" -ForegroundColor Green
Write-Host "     Proveedor:          $NombreProveedor ($LMSTUDIO_URL)"
Write-Host "     Archivo:            $CONFIG_FILE"
Write-Host "     Modelo por defecto: $ClaveProveedor/$DefaultModel"
Write-Host ""
Write-Host "Para cambiar de modelo en OpenCode, usa /models"
Write-Host ""
