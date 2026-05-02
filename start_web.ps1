# Chạy web Seller Management — cài gói (mirror Trung Quốc nếu PyPI chậm) rồi khởi động Flask.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Seller Management System ===" -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Tao virtualenv .venv ..."
    py -3 -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

Write-Host "Cai dat packages (co the vai phut)..."
pip install -r requirements.txt --default-timeout=300
if ($LASTEXITCODE -ne 0) {
    Write-Host "Thu mirror Tsinghua..." -ForegroundColor Yellow
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=300
}

Write-Host ""
Write-Host "Khoi dong server: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Kiem tra DB:      http://127.0.0.1:5000/health/db" -ForegroundColor Green
Write-Host ""

$env:FLASK_APP = "app.py"
py -3 -m flask run --host=127.0.0.1 --port=5000 --debug
