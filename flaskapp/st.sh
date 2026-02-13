#!/bin/bash
# Запускаем Gunicorn в фоне
gunicorn --bind 127.0.0.1:5000 wsgi:app &
APP_PID=$!
sleep 10
echo "Running client tests"
python3 client.py
CLIENT_EXIT=$?
sleep 2
kill -TERM $APP_PID
echo "Client exit code: $CLIENT_EXIT"
exit $CLIENT_EXIT