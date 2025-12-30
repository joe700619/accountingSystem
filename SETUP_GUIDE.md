# Django 會計系統配置完成！

## 📦 專案結構

```
accountingSystem/
├── .venv/                  # Python 虛擬環境
├── config/                 # Django 專案設定
│   ├── settings.py        # 主設定檔（已配置 PostgreSQL）
│   ├── urls.py            # URL 路由
│   └── wsgi.py            # WSGI 配置
├── accounts/              # 帳戶應用
├── static/                # 靜態文件（CSS, JS, 圖片）
├── media/                 # 用戶上傳文件
├── templates/             # HTML 模板
├── manage.py              # Django 管理命令
├── requirements.txt       # Python 依賴套件
└── DATABASE_README.md     # 資料庫配置說明
```

## ✅ 已完成配置

### 1. 資料庫配置
- ✅ PostgreSQL 資料庫已創建：`accounting_system`
- ✅ 資料庫連接已配置並測試成功
- ✅ 初始資料表已遷移（migrate）

### 2. Django 設定
- ✅ Django 4.2.27 已安裝
- ✅ PostgreSQL 驅動 (psycopg2-binary) 已安裝
- ✅ Django REST Framework 已安裝並配置
- ✅ CORS Headers 已配置
- ✅ 語言設定：繁體中文 (zh-hant)
- ✅ 時區設定：Asia/Taipei

### 3. 應用程式
- ✅ accounts 應用已創建

## 🚀 常用命令

### 啟動虛擬環境
```powershell
.\.venv\Scripts\Activate.ps1
```

### 運行開發伺服器
```powershell
python manage.py runserver
```
訪問：http://localhost:8000

### 創建超級用戶（管理員）
```powershell
python manage.py createsuperuser
```

### 創建新應用
```powershell
python manage.py startapp app_name
```

### 資料庫遷移
```powershell
# 創建遷移文件
python manage.py makemigrations

# 執行遷移
python manage.py migrate

# 查看遷移狀態
python manage.py showmigrations
```

### 收集靜態文件
```powershell
python manage.py collectstatic
```

### 進入 Django Shell
```powershell
python manage.py shell
```

### 進入資料庫 Shell
```powershell
python manage.py dbshell
```

## 🔧 資料庫資訊

- **資料庫名稱**: accounting_system
- **使用者**: postgres
- **密碼**: 5201314Aa
- **主機**: localhost
- **端口**: 5432

## 📝 下一步建議

### 1. 創建超級用戶
```powershell
.\.venv\Scripts\Activate.ps1
python manage.py createsuperuser
```

### 2. 運行開發伺服器
```powershell
python manage.py runserver
```

### 3. 訪問管理介面
打開瀏覽器訪問：http://localhost:8000/admin

### 4. 開始開發
根據您的會計系統需求創建以下應用：
- 會計科目管理（chart of accounts）
- 會計分錄（journal entries）
- 總帳（general ledger）
- 財務報表（financial statements）
- 等等...

## 🛠️ 開發流程示例

### 創建一個新的會計應用
```powershell
python manage.py startapp ledger
```

### 在 config/settings.py 中註冊應用
```python
INSTALLED_APPS = [
    # ...
    'ledger',
]
```

### 定義模型（models.py）
```python
from django.db import models

class Account(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
```

### 創建和執行遷移
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 註冊到管理介面（admin.py）
```python
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'balance']
    search_fields = ['code', 'name']
```

## 📚 有用的資源

- Django 官方文檔：https://docs.djangoproject.com/
- Django REST Framework：https://www.django-rest-framework.org/
- PostgreSQL 文檔：https://www.postgresql.org/docs/

## 🔐 安全提醒

⚠️ **重要**：在生產環境部署前，請確保：
1. 更改 SECRET_KEY
2. 將 DEBUG 設為 False
3. 配置適當的 ALLOWED_HOSTS
4. 使用環境變數管理敏感資訊（密碼、金鑰等）
5. 啟用 HTTPS
6. 配置適當的資料庫備份策略

## ✨ 恭喜！

您的 Django 會計系統已經配置完成，可以開始開發了！
