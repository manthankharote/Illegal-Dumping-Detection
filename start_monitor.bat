@echo off
cd /d "%~dp0"
echo [SYSTEM] Launching Live Monitor securely from the root directory...
python ai_service/live_monitor.py --source youtube --url "https://www.youtube.com/live/5SIWsxZCA-E?si=-dFxhDm0iWj_0map"
pause
