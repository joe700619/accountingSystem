# PostgreSQL Connection Test Script
# Usage: .\test_postgres.ps1

$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$password = (Get-Content -Path "password.txt" -Raw).Trim()
$env:PGPASSWORD = $password

Write-Host "Connecting to PostgreSQL..." -ForegroundColor Cyan
& $psqlPath -U postgres -c "SELECT version();"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Connection successful!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Connection failed" -ForegroundColor Red
}

Remove-Item Env:\PGPASSWORD
