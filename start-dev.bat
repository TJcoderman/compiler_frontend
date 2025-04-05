@echo off
start cmd /k "cd backend && python manage.py runserver"
start cmd /k "cd frontend && python -m http.server 5500"
start http://localhost:5500/
