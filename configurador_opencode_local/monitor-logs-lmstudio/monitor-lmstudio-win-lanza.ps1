# Lanzador PowerShell para LMStudio Monitor en Windows (con entorno virtual)
# Uso: .\monitor-lmstudio-win-lanza.ps1 [--interval 2] [--theme dracula] [--file ...] [--logs-dir ...]
#      .\monitor-lmstudio-win-lanza.ps1 -RecrearVenv  (fuerza recrear .venv)
# Crea .venv junto al script, instala dependencias y lanza el monitor con ese Python.
# Forzar UTF-8 en consola (evita simbolos raros en Windows PowerShell 5.1)
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
    if ($PSVersionTable.PSVersion.Major -lt 6) { chcp 65001 > $null }
} catch { }

$ScriptDir = Split-Path -Parent $PSCommandPath
$Monitor = Join-Path $ScriptDir "lmstudio-monitor.py"
$Requirements = Join-Path $ScriptDir "requirements.txt"
$VenvDir = Join-Path $ScriptDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

# Flag opcional solo del lanzador (no se pasa al monitor)
$Recrear = $false
$MonitorArgs = @()
foreach ($a in $args) {
    if ($a -eq "-RecrearVenv" -or $a -eq "--recrear-venv" -or $a -eq "/recrear-venv") {
        $Recrear = $true
    } else {
        $MonitorArgs += $a
    }
}

if (-not (Test-Path -LiteralPath $Monitor)) {
    Write-Host "[ERROR] No se encuentra $Monitor" -ForegroundColor Red
    exit 1
}

# 1. Localizar Python base (py launcher preferido en Windows)
$PyCmd = $null
foreach ($c in @("py", "python")) {
    try {
        $null = Get-Command $c -ErrorAction Stop
        # Verificar que realmente ejecuta
        & $c --version > $null 2>&1
        if ($LASTEXITCODE -eq 0) { $PyCmd = $c; break }
    } catch { }
}
if (-not $PyCmd) {
    Write-Host "[ERROR] No se encontro 'py' ni 'python' en el PATH." -ForegroundColor Red
    Write-Host "        Instala Python 3.10+ desde https://www.python.org/downloads/ marcando 'Add python.exe to PATH'."
    exit 1
}

# 2. Crear .venv si no existe o si se pide recrear
if ($Recrear -and (Test-Path -LiteralPath $VenvDir)) {
    Write-Host "Recreando entorno virtual en $VenvDir ..."
    Remove-Item -LiteralPath $VenvDir -Recurse -Force -ErrorAction SilentlyContinue
}
if (-not (Test-Path -LiteralPath $VenvPython)) {
    Write-Host "Creando entorno virtual en $VenvDir (con $PyCmd) ..."
    & $PyCmd -m venv $VenvDir
    if ((-not (Test-Path -LiteralPath $VenvPython)) -or ($LASTEXITCODE -ne 0)) {
        Write-Host "[ERROR] No se pudo crear .venv. Prueba:" -ForegroundColor Red
        Write-Host "        $PyCmd -m ensurepip --upgrade"
        Write-Host "        $PyCmd -m venv `"$VenvDir`""
        exit 1
    }
}

# 3. Instalar dependencias si hace falta (venv nuevo, rich ausente o requirements mas reciente)
$NecesitaInstalar = $false
$Marcador = Join-Path $VenvDir ".requirements-ok.txt"
& $VenvPython -c "import rich" > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    $NecesitaInstalar = $true
} elseif ((Test-Path -LiteralPath $Requirements)) {
    if ((-not (Test-Path -LiteralPath $Marcador)) -or ((Get-Item $Requirements).LastWriteTime -gt (Get-Item $Marcador).LastWriteTime)) {
        $NecesitaInstalar = $true
    }
}
if ($NecesitaInstalar) {
    Write-Host "Instalando dependencias en .venv ..."
    & $VenvPython -m pip install --upgrade pip
    if (Test-Path -LiteralPath $Requirements) {
        & $VenvPython -m pip install -r $Requirements
    } else {
        & $VenvPython -m pip install "rich>=13.0.0"
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Fallo 'pip install'. Prueba manualmente:" -ForegroundColor Red
        Write-Host "        & `"$VenvPython`" -m pip install -r `"$Requirements`""
        exit 1
    }
    # Marcar instalacion correcta para no reinstalar en cada arranque
    try { Set-Content -LiteralPath $Marcador -Value (Get-Date).ToString("o") -Encoding UTF8 } catch { }
}

# 4. Lanzar el monitor con el Python del venv (propaga codigo de salida)
& $VenvPython -u $Monitor @MonitorArgs
exit $LASTEXITCODE
