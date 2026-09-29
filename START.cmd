@echo off
setlocal
cd /d "%~dp0"
if /I "%~1"=="--check" goto check
if /I "%~1"=="--check-tabpfn" goto check_tabpfn
if /I "%~1"=="--verify-further" set "EXAM_MODE=3"
if /I "%~1"=="--verify-further" goto ensure_main_env
if /I "%~1"=="--predict-tabpfn" set "EXAM_MODE=4"
if /I "%~1"=="--predict-tabpfn" set "PREDICT_INPUT=%~2"
if /I "%~1"=="--predict-tabpfn" goto tabpfn_dependencies

echo 1 - Atidaryti JupyterLab
echo 2 - Pakartoti pradini eksperimenta (apie 27 min.)
echo 3 - Patikrinti papildomu bandymu rezultatus (be permokymo)
echo 4 - Atpazinti nauja irasa su TabPFN v2
choice /C 1234 /N /M "Pasirinkite 1, 2, 3 arba 4: "
set "EXAM_MODE=%ERRORLEVEL%"
if "%EXAM_MODE%"=="4" goto tabpfn_dependencies

:ensure_main_env
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
if "%EXAM_MODE%"=="3" goto verify_further
".venv\Scripts\python.exe" -c "import jupyterlab, ipykernel" >nul 2>&1
if not errorlevel 1 goto lab
".venv\Scripts\python.exe" -m pip install jupyterlab ipykernel
if errorlevel 1 goto failed
:lab
".venv\Scripts\python.exe" start_jupyter.py
if errorlevel 1 goto failed
exit /b 0

:experiment
echo Pakartojamas istorinis pagrindinis bandymas. Nauji papildomi bandymai neperrasomi.
echo Nauji results\main rezultatai pakeis ankstesnius results\main failus.
".venv\Scripts\python.exe" run_experiment.py --config configs/main.yaml
if errorlevel 1 goto failed
echo Baigta. Ataskaita: results\main\report.md
pause
exit /b 0

:verify_further
echo Tikrinami jau issaugoti triju papildomu modeliu 50 isoriniu skaidiniu rezultatai...
".venv\Scripts\python.exe" verify_next_20260928.py --read-only
if errorlevel 1 goto failed
echo Patikra baigta. Issaugotos suvestines: results\further_20260928\
if /I "%~1"=="--verify-further" exit /b 0
pause
exit /b 0

:tabpfn_dependencies
set "TABPFN_PY=%~dp0.venv_tabpfn\Scripts\python.exe"
if exist "%TABPFN_PY%" goto tabpfn_check
set "TABPFN_PY=%USERPROFILE%\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn\Scripts\python.exe"
if exist "%TABPFN_PY%" goto tabpfn_check
goto create_tabpfn_env

:tabpfn_check
"%TABPFN_PY%" -c "import tabpfn, torch, sklearn, pandas, scipy" >nul 2>&1
if not errorlevel 1 goto tabpfn_predict
goto create_tabpfn_env

:create_tabpfn_env
echo Kuriama atskira TabPFN v2 Python aplinka. Pirma karta reikia interneto.
py -3.10 -m venv .venv_tabpfn
if not errorlevel 1 goto install_tabpfn
python -m venv .venv_tabpfn
if errorlevel 1 goto failed
:install_tabpfn
set "TABPFN_PY=%~dp0.venv_tabpfn\Scripts\python.exe"
"%TABPFN_PY%" -m pip install -r requirements_tabpfn_v2_lock.txt
if errorlevel 1 goto failed

:tabpfn_predict
if not defined PREDICT_INPUT set /p "PREDICT_INPUT=Iveskite JSON failo su 18 pozymiu kelia: "
if not defined PREDICT_INPUT goto failed
if not exist "%PREDICT_INPUT%" goto failed
"%TABPFN_PY%" predict_tabpfn.py --input "%PREDICT_INPUT%"
if errorlevel 1 goto failed
if /I "%~1"=="--predict-tabpfn" exit /b 0
pause
exit /b 0

:check
if not exist ".venv\Scripts\python.exe" exit /b 1
".venv\Scripts\python.exe" -c "import numpy, pandas, scipy, sklearn, matplotlib, yaml, joblib, nbformat, threadpoolctl; print('Python ir pagrindines priklausomybes veikia.')"
exit /b %ERRORLEVEL%

:check_tabpfn
set "TABPFN_PY=%~dp0.venv_tabpfn\Scripts\python.exe"
if not exist "%TABPFN_PY%" set "TABPFN_PY=%USERPROFILE%\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn\Scripts\python.exe"
if not exist "%TABPFN_PY%" exit /b 1
if not exist "results\further_20260928\tabpfn_v2\final_tabpfn_v2.tabpfn_fit" exit /b 1
if not exist "results\further_20260928\tabpfn_v2\final_model_metadata.json" exit /b 1
"%TABPFN_PY%" -c "import tabpfn, torch, sklearn, pandas, scipy; print('TabPFN v2 aplinka veikia.')"
exit /b %ERRORLEVEL%

:failed
echo Nepavyko. Klaidos priezastis parodyta auksciau.
echo Jei Python neirasytas, idiekite Python 3.10 ir bandykite dar karta.
if not "%~1"=="" exit /b 1
pause
exit /b 1
