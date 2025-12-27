@echo off
if "%~1"=="" (
    python "%~dp0scripts\shell.py"
) else (
    python "%~dp0scripts\shell.py" %*
)