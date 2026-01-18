@echo off
REM Script to record API traffic using Keploy on Windows
REM Usage: scripts\keploy-record.bat

echo Starting Keploy in record mode...
echo Make sure Keploy server is running: keploy
echo.
echo Starting FastAPI application through Keploy proxy...
echo API will be available at: http://localhost:8080
echo Press Ctrl+C to stop recording
echo.

keploy record -c "uvicorn app.main:app --host 0.0.0.0 --port 8000"
