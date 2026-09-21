@echo off
setlocal
cd /d "%~dp0"
if /I "%~1"=="--check" goto check

echo 1 - Atidaryti JupyterLab
echo 2 - Pakartoti visa eksperimenta (apie 27 min.)
choice /C 12 /N /M "Pasirinkite 1 arba 2: "
set "EXAM_MODE=%ERRORLEVEL%"

if exist ".venv\Scripts\python.exe" goto dependencies
echo Kuriama Python aplinka...
py -3.10 -m venv .venv
if not errorlevel 1 goto dependencies
python -m venv .venv
if errorlevel 1 goto failed

:dependencies
".venv\Scripts\python.exe" -c "import numpy, pandas, scipy, sklearn, matplotlib, yaml, joblib, nbformat, threadpoolctl" >nul 2>&1
if not errorlevel 1 goto run
echo Diegiamos priklausomybes. Pirma karta reikia interneto.
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed

:run
if "%EXAM_MODE%"=="2" goto experiment
".venv\Scripts\python.exe" -c "import jupyterlab, ipykernel" >nul 2>&1
if not errorlevel 1 goto lab
".venv\Scripts\python.exe" -m pip install jupyterlab ipykernel
if errorlevel 1 goto failed
:lab
".venv\Scripts\python.exe" -m jupyterlab
if errorlevel 1 goto failed
exit /b 0

:experiment
echo Nauji rezultatai pakeis results\main turini.
".venv\Scripts\python.exe" run_experiment.py --config configs/main.yaml
if errorlevel 1 goto failed
echo Baigta. Ataskaita: results\main\report.md
pause
exit /b 0

:check
if not exist ".venv\Scripts\python.exe" exit /b 1
".venv\Scripts\python.exe" -c "import numpy, pandas, scipy, sklearn, matplotlib, yaml, joblib, nbformat, threadpoolctl; print('Python ir pagrindines priklausomybes veikia.')"
exit /b %ERRORLEVEL%

:failed
echo Nepavyko. Klaidos priezastis parodyta auksciau.
echo Jei Python neirasytas, idiekite Python 3.10 ir bandykite dar karta.
pause
exit /b 1
