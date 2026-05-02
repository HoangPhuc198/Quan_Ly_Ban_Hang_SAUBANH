@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo === Seller Management System ===

if not exist ".venv\Scripts\python.exe" (
    echo Tao virtualenv .venv ...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Loi: khong tao duoc venv. Thu cai Python tu python.org
        pause
        exit /b 1
    )
)

echo Cai packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt --default-timeout=300
if errorlevel 1 (
    echo Pip loi - kiem tra mang hoac chay lai.
    pause
    exit /b 1
)

echo.
echo Mo trinh duyet: http://127.0.0.1:5000
echo Kiem tra DB: http://127.0.0.1:5000/health/db
echo.

".venv\Scripts\python.exe" app.py
pause
