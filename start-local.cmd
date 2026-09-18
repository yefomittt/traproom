@echo off
cd /d "%~dp0"
set "TRAPROOM_PY=%~dp0.venv\Scripts\python.exe"
if not exist "%TRAPROOM_PY%" set "TRAPROOM_PY=%~dp0..\..\work\music-venv\Scripts\python.exe"
if not exist "%TRAPROOM_PY%" (
  echo Python environment not found. See README.md.
  pause
  exit /b 1
)
echo Traproom: http://127.0.0.1:8765/
echo Login details: local-access.txt
echo Keep this window open. Ctrl+C stops the server.
"%TRAPROOM_PY%" manage.py runserver 127.0.0.1:8765 --noreload
pause
