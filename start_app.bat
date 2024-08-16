@echo off

REM Activate the Python virtual environment
call StayHappyWebApp\.venv\Scripts\activate

REM Start the .NET application in a new window
start "" dotnet run --project StayHappyWebApp\StayHappyWebApp.csproj

REM Wait for a moment to ensure the .NET application starts properly (optional)
timeout /t 2 /nobreak

REM Navigate to the directory containing the Python script and run it
cd StayHappyWebApp\Scripts\python
py main.py

REM Return to the original directory (optional)
cd ..\..

REM Pause to keep the command window open for any potential output (optional)
pause
