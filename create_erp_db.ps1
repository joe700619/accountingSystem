# 快速建立 ERP 資料庫腳本
# 使用方法: .\create_erp_db.ps1

# 從 .env 讀取密碼
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $passwordLine = $envContent | Where-Object { $_ -match "^DB_PASSWORD=" }
    if ($passwordLine) {
        $password = ($passwordLine -split "=", 2)[1].Trim()
        $env:PGPASSWORD = $password
    }
}

$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"

# 建立資料庫
& $psqlPath -U postgres -c "CREATE DATABASE erp_db WITH ENCODING 'UTF8';"

if ($LASTEXITCODE -eq 0) {
    Write-Host "資料庫 erp_db 建立成功！" -ForegroundColor Green
}
else {
    Write-Host "建立失敗 - 資料庫可能已存在" -ForegroundColor Yellow
}

# 清除密碼環境變數
Remove-Item Env:\PGPASSWORD
