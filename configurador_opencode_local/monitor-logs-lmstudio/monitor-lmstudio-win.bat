@echo off
REM Lanzador Windows para LMStudio Monitor (doble clic o desde cmd)
REM Usa 'py' si existe, si no 'python'. Reenvia todos los argumentos.
chcp 65001 > nul 2>&1
setlocal
set "PYCMD=py"
where py > nul 2>&1
if errorlevel 1 set "PYCMD=python"
%PYCMD% -u "%~dp0lmstudio-monitor.py" %*
endlocal
