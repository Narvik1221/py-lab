@echo off
cd ..
echo Starting Waitress server from project root...
waitress-serve --host=127.0.0.1 --port=5000 flaskapp.wsgi:app
timeout /t 10 /nobreak > nul
cd flaskapp
echo Running client tests...
python client.py
set CLIENT_EXIT=%errorlevel%
cd ..
timeout /t 2 /nobreak > nul
taskkill /F /IM waitress-serve.exe > nul 2>&1
exit /b %CLIENT_EXIT%