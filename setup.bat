@echo off
title NutriGuide AI — Setup Wizard
color 0B

echo.
echo  ======================================================
echo    NutriGuide AI — First-Time Setup Wizard
echo    IBM Granite Nutrition Agent
echo  ======================================================
echo.

:: ─── Collect IBM watsonx.ai credentials ─────────────────────
echo  This wizard will configure your IBM watsonx.ai credentials.
echo  You need these to use IBM Granite LLM (live mode).
echo  Without credentials, the app still works in Demo mode.
echo.
echo  Get your credentials at: https://cloud.ibm.com/
echo.

set /p APIKEY=  Enter your IBM Cloud API Key (or press Enter to skip): 
set /p PROJID=  Enter your watsonx.ai Project ID (or press Enter to skip): 
set /p REGION=  Enter region [us-south/eu-gb/jp-tok] (default: us-south): 

if "%REGION%"=="" set REGION=us-south

set URL=https://%REGION%.ml.cloud.ibm.com

:: ─── Write .env file ─────────────────────────────────────────
echo.
echo  Writing configuration to .env...

(
echo # IBM watsonx.ai Credentials
echo WATSONX_API_KEY=%APIKEY%
echo WATSONX_PROJECT_ID=%PROJID%
echo WATSONX_URL=%URL%
echo.
echo # App Settings
echo FLASK_SECRET_KEY=nutriguide-secret-%RANDOM%
echo FLASK_PORT=5000
echo FLASK_DEBUG=False
) > .env

echo  [OK] .env file written.
echo.

:: ─── Run the app ─────────────────────────────────────────────
set /p RUNOW=  Start the app now? [Y/n]: 
if /i "%RUNOW%"=="n" goto end

call run.bat
goto done

:end
echo.
echo  Setup complete! Run run.bat whenever you want to start NutriGuide AI.
echo.

:done
pause
