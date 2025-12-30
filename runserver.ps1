# Django 開發伺服器啟動腳本
# Usage: .\runserver.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "啟動 Django 會計系統開發伺服器" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 啟動虛擬環境並運行伺服器
.\.venv\Scripts\Activate.ps1

Write-Host "檢查資料庫連接..." -ForegroundColor Yellow
python manage.py check --database default

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "資料庫連接正常！" -ForegroundColor Green
    Write-Host ""
    Write-Host "啟動開發伺服器..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "伺服器地址：http://localhost:8000" -ForegroundColor Cyan
    Write-Host "管理後台：http://localhost:8000/admin" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "按 Ctrl+C 停止伺服器" -ForegroundColor Gray
    Write-Host ""
    
    python manage.py runserver
}
else {
    Write-Host ""
    Write-Host "資料庫連接失敗！請檢查配置。" -ForegroundColor Red
}
