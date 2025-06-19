@echo off
:: ==============================================
:: Virtual Intelligence Environment Runner
:: Works in CMD and can be run from PowerShell
:: ==============================================

echo ========================================
echo     Virtual Intelligence Launcher
echo ========================================
echo.

echo Select what to run:
echo 1. core_module - Virtual Intelligence Server
echo 2. tool_script - Helper Tools
echo 3. tests - Unit Tests
echo.

set /p choice=Enter 1, 2 or 3: 

if "%choice%"=="1" (
    echo.
    echo [INFO] Running Virtual Intelligence Server...
    python core_module/main.py
    goto :eof
)

if "%choice%"=="2" (
    echo.
    echo [INFO] Listing helper tools:
    for %%f in (tool_script\*.py) do echo   - %%~nf
    goto :eof
)

if "%choice%"=="3" (
    echo.
    echo [INFO] Listing tests:
    for %%f in (tests\*.py) do echo   - %%~nf
    goto :eof
)

echo.
echo [ERROR] Invalid choice. Please enter 1, 2, or 3.
pause
