# 環境變數設置指南

## 概述

本專案使用 `.env` 文件來管理敏感信息（如資料庫密碼、Django SECRET_KEY 等），確保這些信息不會被推送到 GitHub。

## 快速設置步驟

### 1. 創建 `.env` 文件

複製 `.env.example` 並重命名為 `.env`：

```powershell
Copy-Item .env.example .env
```

### 2. 編輯 `.env` 文件

打開 `.env` 文件並填入你的實際配置：

```bash
# 資料庫設定
DB_NAME=accounting_system
DB_USER=postgres
DB_PASSWORD=你的資料庫密碼
DB_HOST=localhost
DB_PORT=5432

# Django 設定
SECRET_KEY=你的 Django Secret Key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS 設定
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. 安裝依賴

確保已安裝 `python-decouple`：

```powershell
pip install -r requirements.txt
```

## 文件說明

### `.env` (本地文件，不會被推送到 Git)
- 包含你的**實際密碼和敏感信息**
- 已被加入 `.gitignore`，不會上傳到 GitHub
- **每個開發者需要自己創建此文件**

### `.env.example` (範本文件，會被推送到 Git)
- 包含環境變數的**範本和說明**
- 使用佔位符（placeholder）而非實際密碼
- 幫助其他開發者了解需要哪些環境變數

## 使用說明

### Django 配置

`config/settings.py` 已更新為使用環境變數：

```python
from decouple import config

# 從 .env 文件讀取配置
SECRET_KEY = config('SECRET_KEY', default='...')
DEBUG = config('DEBUG', default=True, cast=bool)
DATABASES = {
    'default': {
        'NAME': config('DB_NAME', default='accounting_system'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD'),  # 必須在 .env 中設置
        ...
    }
}
```

### 資料庫設置腳本

`setup_database.ps1` 已更新為從 `.env` 讀取密碼：

```powershell
# 自動從 .env 讀取 DB_PASSWORD
.\setup_database.ps1
```

## 安全最佳實踐

✅ **DO（應該做的）：**
- 在 `.env` 中存儲所有敏感信息
- 定期更換密碼和 SECRET_KEY
- 使用強密碼（包含大小寫字母、數字、特殊符號）
- 確保 `.env` 已在 `.gitignore` 中

❌ **DON'T（不應該做的）：**
- 不要把 `.env` 文件推送到 Git
- 不要在程式碼中硬編碼密碼
- 不要在 `.env.example` 中使用真實密碼
- 不要透過聊天工具分享 `.env` 內容

## 生成新的 SECRET_KEY

如果需要生成新的 Django SECRET_KEY：

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

或在 PowerShell 中：

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 團隊協作

當新成員加入專案時：

1. Clone 專案
2. 複製 `.env.example` 為 `.env`
3. 向團隊負責人索取實際的配置值
4. 填入 `.env` 文件中
5. 運行 `pip install -r requirements.txt`

## 故障排除

### 問題：找不到 .env 文件

**解決方案：**
```powershell
Copy-Item .env.example .env
# 然後編輯 .env 填入實際配置
```

### 問題：setup_database.ps1 報錯

**錯誤訊息：** "錯誤：找不到 .env 文件！"

**解決方案：** 確保專案根目錄有 `.env` 文件

### 問題：Django 無法連接資料庫

**解決方案：** 檢查 `.env` 中的 `DB_PASSWORD` 是否正確

## 相關文件

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 完整的系統設置指南
- [DATABASE_README.md](DATABASE_README.md) - 資料庫配置說明
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub 設置指南
