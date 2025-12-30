# GitHub 推送設置腳本
# Usage: .\push_to_github.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "GitHub 推送設置" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 提示用戶輸入倉庫資訊
$username = Read-Host "請輸入您的 GitHub 用戶名"
$repoName = Read-Host "請輸入倉庫名稱（預設: accountingSystem）"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "accountingSystem"
}

# 詢問使用 HTTPS 還是 SSH
Write-Host ""
Write-Host "選擇連接方式:" -ForegroundColor Yellow
Write-Host "1. HTTPS (需要 Personal Access Token)"
Write-Host "2. SSH (需要先設置 SSH 金鑰)"
$choice = Read-Host "請選擇 (1/2)"

if ($choice -eq "2") {
    $repoUrl = "git@github.com:$username/$repoName.git"
}
else {
    $repoUrl = "https://github.com/$username/$repoName.git"
}

Write-Host ""
Write-Host "將添加遠程倉庫: $repoUrl" -ForegroundColor Yellow
Write-Host ""

# 檢查是否已有 remote
$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    Write-Host "遠程倉庫已存在: $existingRemote" -ForegroundColor Yellow
    $replace = Read-Host "是否要替換？(y/N)"
    
    if ($replace -eq "y" -or $replace -eq "Y") {
        git remote remove origin
        Write-Host "已移除舊的遠程倉庫" -ForegroundColor Green
    }
    else {
        Write-Host "操作已取消" -ForegroundColor Red
        exit
    }
}

# 添加遠程倉庫
Write-Host "正在添加遠程倉庫..." -ForegroundColor Yellow
git remote add origin $repoUrl

if ($LASTEXITCODE -eq 0) {
    Write-Host "遠程倉庫添加成功！" -ForegroundColor Green
    Write-Host ""
    
    # 顯示遠程倉庫
    Write-Host "遠程倉庫列表:" -ForegroundColor Cyan
    git remote -v
    Write-Host ""
    
    # 檢查當前分支
    $branch = git branch --show-current
    Write-Host "當前分支: $branch" -ForegroundColor Cyan
    Write-Host ""
    
    # 詢問是否立即推送
    $push = Read-Host "是否要立即推送到 GitHub？(Y/n)"
    
    if ($push -ne "n" -and $push -ne "N") {
        Write-Host ""
        Write-Host "正在推送到 GitHub..." -ForegroundColor Yellow
        
        if ($choice -eq "1") {
            Write-Host ""
            Write-Host "提示：如果提示輸入密碼，請使用 Personal Access Token" -ForegroundColor Yellow
            Write-Host "Token 獲取：https://github.com/settings/tokens" -ForegroundColor Cyan
            Write-Host ""
        }
        
        git push -u origin $branch
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host "推送成功！" -ForegroundColor Green
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "倉庫地址: https://github.com/$username/$repoName" -ForegroundColor Cyan
            Write-Host ""
        }
        else {
            Write-Host ""
            Write-Host "推送失敗！" -ForegroundColor Red
            Write-Host ""
            Write-Host "可能的原因：" -ForegroundColor Yellow
            Write-Host "1. 認證失敗 - 需要使用 Personal Access Token 或 SSH 金鑰"
            Write-Host "2. 倉庫不存在 - 請先在 GitHub 上創建倉庫"
            Write-Host "3. 網絡問題 - 檢查網絡連接"
            Write-Host ""
            Write-Host "詳細說明請參考 GITHUB_SETUP.md" -ForegroundColor Cyan
        }
    }
    else {
        Write-Host ""
        Write-Host "設置完成！您可以稍後使用以下命令推送：" -ForegroundColor Green
        Write-Host "git push -u origin $branch" -ForegroundColor White
    }
}
else {
    Write-Host "添加遠程倉庫失敗！" -ForegroundColor Red
    Write-Host "請檢查 Git 是否正確安裝" -ForegroundColor Yellow
}
