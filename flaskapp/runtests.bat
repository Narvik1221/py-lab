@echo off
echo Starting Gunicorn server...
start /B gunicorn --bind 127.0.0.1:5000 wsgi:app
timeout /t 10 /nobreak > nul
echo Running client tests...
python client.py
set CLIENT_EXIT=%errorlevel%
timeout /t 2 /nobreak > nul
taskkill /F /IM gunicorn.exe > nul 2>&1
echo Client exit code: %CLIENT_EXIT%
exit /b %CLIENT_EXIT%