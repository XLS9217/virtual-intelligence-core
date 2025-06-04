@echo off

:: Check if conda is available
where conda >nul 2>nul
if %errorlevel%==0 (
    echo Conda found.

    :: Check if a conda environment is active
    if defined CONDA_DEFAULT_ENV (
        echo Deactivating conda environment: %CONDA_DEFAULT_ENV%
        call conda deactivate
    )
)

:: Check if a virtual environment is already active
if defined VIRTUAL_ENV (
    echo Virtual environment already active: %VIRTUAL_ENV%
) else (
    :: Activate .venv only if it exists
    if exist ".venv\Scripts\activate.bat" (
        echo Activating .venv...
        call .venv\Scripts\activate.bat
    ) else (
        echo .venv\Scripts\activate.bat not found.
    )
)

call python -m core_module
