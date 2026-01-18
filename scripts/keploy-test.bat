@echo off
REM Script to replay recorded tests using Keploy on Windows
REM Usage: scripts\keploy-test.bat

echo Starting Keploy in test mode...
echo Make sure Keploy server is running: keploy
echo Make sure your FastAPI application is running on port 8000
echo.

keploy test -c "echo App should be running on port 8000" --delay 10
