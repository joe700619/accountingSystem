# GitHub 推送指南

## 🔍 問題診斷

您的 Git 倉庫已經初始化，但**尚未設置遠程倉庫（remote）**。

當前狀態：
- ✅ Git 倉庫已初始化
- ✅ 有一個提交 (v0)
- ❌ 沒有設置遠程倉庫（remote）

---

## 📝 解決方案

### 步驟 1: 在 GitHub 上創建倉庫

1. 前往 https://github.com/new
2. 填寫倉庫資訊：
   - **Repository name**: `accountingSystem` 或您想要的名稱
   - **Description**: Django 會計系統
   - **Public/Private**: 選擇公開或私有
   - ⚠️ **不要**勾選 "Initialize this repository with a README"
   - ⚠️ **不要**添加 .gitignore 或 LICENSE（我們已經有了）
3. 點擊 "Create repository"

### 步驟 2: 添加遠程倉庫

GitHub 會顯示一些命令。使用以下命令添加遠程倉庫：

```powershell
# 替換成您的 GitHub 用戶名和倉庫名
git remote add origin https://github.com/YOUR_USERNAME/accountingSystem.git

# 確認遠程倉庫已添加
git remote -v
```

**或者使用 SSH（如果已設置 SSH 金鑰）：**
```powershell
git remote add origin git@github.com:YOUR_USERNAME/accountingSystem.git
```

### 步驟 3: 推送到 GitHub

```powershell
# 推送主分支到 GitHub
git push -u origin main

# 或者，如果您的分支名是 master
git push -u origin master
```

---

## 🚀 完整命令流程

假設您的 GitHub 用戶名是 `yourname`：

```powershell
# 1. 添加遠程倉庫
git remote add origin https://github.com/yourname/accountingSystem.git

# 2. 確認分支名稱
git branch

# 3. 推送（首次推送使用 -u 參數）
git push -u origin main
```

---

## ⚠️ 可能遇到的問題

### 問題 1: 認證失敗

**錯误訊息：**
```
remote: Support for password authentication was removed...
```

**解決方案：**
GitHub 已不再支援密碼認證。您需要使用：

#### 選項 A: Personal Access Token (推薦)

1. 前往 https://github.com/settings/tokens
2. 點擊 "Generate new token" → "Generate new token (classic)"
3. 設定範圍：勾選 `repo`
4. 生成並複製 token（只會顯示一次！）
5. 在推送時，使用 token 代替密碼

#### 選項 B: SSH 金鑰

1. 生成 SSH 金鑰：
   ```powershell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. 複製公鑰：
   ```powershell
   Get-Content ~/.ssh/id_ed25519.pub | clip
   ```
3. 前往 https://github.com/settings/keys
4. 點擊 "New SSH key"，貼上公鑰
5. 使用 SSH URL：
   ```powershell
   git remote set-url origin git@github.com:yourname/accountingSystem.git
   ```

### 問題 2: 遠程倉庫已存在

**錯誤訊息：**
```
fatal: remote origin already exists
```

**解決方案：**
```powershell
# 刪除現有的 remote
git remote remove origin

# 重新添加
git remote add origin https://github.com/yourname/accountingSystem.git
```

### 問題 3: 文件太大

如果 push 失敗，提示文件太大，檢查 `.gitignore` 是否正確：

```powershell
# 確認 .venv 被忽略
git check-ignore .venv
# 應該輸出: .venv

# 如果不小心添加了虛擬環境，移除它：
git rm -r --cached .venv
git commit -m "Remove .venv from git"
```

### 問題 4: 分支名稱不匹配

**錯誤訊息：**
```
error: src refspec main does not match any
```

**解決方案：**
```powershell
# 檢查當前分支名
git branch

# 如果是 master，使用：
git push -u origin master

# 或者重命名分支為 main：
git branch -M main
git push -u origin main
```

---

## 📋 完整設置腳本

創建一個 `push_to_github.ps1` 腳本：

```powershell
# GitHub 推送設置腳本
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

$repoUrl = "https://github.com/$username/$repoName.git"

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
    } else {
        Write-Host "操作已取消" -ForegroundColor Red
        exit
    }
}

# 添加遠程倉庫
git remote add origin $repoUrl

if ($LASTEXITCODE -eq 0) {
    Write-Host "遠程倉庫添加成功！" -ForegroundColor Green
    Write-Host ""
    
    # 檢查當前分支
    $branch = git branch --show-current
    Write-Host "當前分支: $branch" -ForegroundColor Cyan
    Write-Host ""
    
    # 推送
    Write-Host "正在推送到 GitHub..." -ForegroundColor Yellow
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=====================================" -ForegroundColor Green
        Write-Host "推送成功！" -ForegroundColor Green
        Write-Host "=====================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "倉庫地址: https://github.com/$username/$repoName" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "推送失敗！" -ForegroundColor Red
        Write-Host "如果遇到認證問題，請參考 GITHUB_SETUP.md" -ForegroundColor Yellow
    }
} else {
    Write-Host "添加遠程倉庫失敗！" -ForegroundColor Red
}
```

---

## 🔐 認證設置（重要）

### 使用 Personal Access Token

當推送時提示輸入密碼，使用 Personal Access Token：

1. 生成 Token：https://github.com/settings/tokens
2. 範圍選擇：`repo`
3. 保存 token（重要！只顯示一次）
4. 推送時：
   - Username: 您的 GitHub 用戶名
   - Password: 貼上 token（不是您的密碼！）

### 使用 GitHub CLI（推薦）

```powershell
# 安裝 GitHub CLI
winget install --id GitHub.cli

# 登入
gh auth login

# 推送
git push -u origin main
```

---

## ✅ 驗證推送成功

推送成功後，訪問：
```
https://github.com/YOUR_USERNAME/accountingSystem
```

您應該能看到所有文件！

---

## 📚 後續操作

### 克隆倉庫（其他電腦）
```powershell
git clone https://github.com/yourname/accountingSystem.git
cd accountingSystem
```

### 日常更新流程
```powershell
# 1. 查看狀態
git status

# 2. 添加更改
git add .

# 3. 提交
git commit -m "描述您的更改"

# 4. 推送
git push
```

---

## 💡 提示

- 🔒 **密碼文件安全**：`password.txt` 已在 `.gitignore` 中，不會被推送
- 📦 **虛擬環境**：`.venv` 也被忽略，不會上傳
- 🔑 **敏感資訊**：確保 `.env` 在 `.gitignore` 中
- 📝 **提交訊息**：使用清晰的提交訊息描述更改

---

需要幫助？請告訴我遇到的具體錯誤訊息！
