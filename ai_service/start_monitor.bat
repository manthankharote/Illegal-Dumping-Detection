@echo off
cd /d "%~dp0\.."
echo [SYSTEM] Correcting directory path and launching Live Monitor...
python ai_service/live_monitor.py --source youtube --url "https://www.youtube.com/live/5SIWsxZCA-E?si=-dFxhDm0iWj_0map"
pause
