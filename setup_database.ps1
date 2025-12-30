# 會計系統資料庫設置腳本
# Usage: .\setup_database.ps1

$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$password = (Get-Content -Path "password.txt" -Raw).Trim()
$env:PGPASSWORD = $password

$dbName = "accounting_system"
$dbUser = "postgres"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "會計系統資料庫設置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查資料庫是否已存在
Write-Host "檢查資料庫是否存在..." -ForegroundColor Yellow
$checkCmd = "SELECT 1 FROM pg_database WHERE datname = '" + $dbName + "';"
$checkDb = & $psqlPath -U $dbUser -tc $checkCmd

if ($checkDb -match "1") {
    Write-Host "資料庫已經存在。" -ForegroundColor Green
    Write-Host ""
    $response = Read-Host "是否要刪除並重新創建？(y/N)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "正在刪除現有資料庫..." -ForegroundColor Yellow
        $dropCmd = "DROP DATABASE " + $dbName + ";"
        & $psqlPath -U $dbUser -c $dropCmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "資料庫已刪除。" -ForegroundColor Green
        }
        else {
            Write-Host "刪除資料庫失敗！" -ForegroundColor Red
            Remove-Item Env:\PGPASSWORD
            exit 1
        }
    }
    else {
        Write-Host "保留現有資料庫，結束設置。" -ForegroundColor Yellow
        Remove-Item Env:\PGPASSWORD
        exit 0
    }
}

# 創建資料庫
Write-Host ""
Write-Host "正在創建資料庫..." -ForegroundColor Yellow
$createCmd = "CREATE DATABASE " + $dbName + " WITH ENCODING 'UTF8';"
& $psqlPath -U $dbUser -c $createCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "資料庫創建成功！" -ForegroundColor Green
}
else {
    Write-Host "資料庫創建失敗！" -ForegroundColor Red
    Remove-Item Env:\PGPASSWORD
    exit 1
}

# 驗證資料庫
Write-Host ""
Write-Host "驗證資料庫連接..." -ForegroundColor Yellow
& $psqlPath -U $dbUser -d $dbName -c "SELECT current_database();"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "資料庫設置完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "資料庫名稱: accounting_system" -ForegroundColor Cyan
    Write-Host "使用者: postgres" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Django settings.py 設定範例:" -ForegroundColor Yellow
    Write-Host "DATABASES = {" -ForegroundColor White
    Write-Host "    'default': {" -ForegroundColor White
    Write-Host "        'ENGINE': 'django.db.backends.postgresql'," -ForegroundColor White
    Write-Host "        'NAME': 'accounting_system'," -ForegroundColor White
    Write-Host "        'USER': 'postgres'," -ForegroundColor White
    Write-Host "        'PASSWORD': '5201314Aa'," -ForegroundColor White
    Write-Host "        'HOST': 'localhost'," -ForegroundColor White
    Write-Host "        'PORT': '5432'," -ForegroundColor White
    Write-Host "    }" -ForegroundColor White
    Write-Host "}" -ForegroundColor White
}
else {
    Write-Host "資料庫驗證失敗！" -ForegroundColor Red
}

Remove-Item Env:\PGPASSWORD
