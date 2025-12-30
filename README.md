# 會計系統 (Accounting System)

Django 會計系統 - 使用 Django 4.2 + PostgreSQL 18

## 🎯 專案狀態

✅ **已完成配置** - 系統已準備好開始開發

## 📋 技術棧

- **後端框架**: Django 4.2.27
- **資料庫**: PostgreSQL 18
- **API**: Django REST Framework
- **語言**: Python 3.14+
- **前端**: 待開發

## 🗂️ 專案結構

```
accountingSystem/
│
├── config/                 # Django 專案設定
│   ├── settings.py        # 主設定檔
│   ├── urls.py            # URL 路由
│   └── wsgi.py            # WSGI 配置
│
├── accounts/              # 帳戶管理應用
│   ├── models.py          # 資料模型
│   ├── views.py           # 視圖
│   ├── admin.py           # 管理介面
│   └── ...
│
├── static/                # 靜態文件（CSS, JS, 圖片）
├── media/                 # 用戶上傳文件
├── templates/             # HTML 模板
│
├── .venv/                 # Python 虛擬環境
├── manage.py              # Django 管理命令
├── requirements.txt       # Python 依賴
│
└── 文檔/
    ├── SETUP_GUIDE.md        # 設置指南
    ├── DATABASE_README.md    # 資料庫說明
    ├── runserver.ps1         # 快速啟動腳本
    └── README.md             # 本文件
```

## 🚀 快速開始

### 1. 啟動虛擬環境
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. 運行開發伺服器
```powershell
# 使用快速啟動腳本
.\runserver.ps1

# 或手動啟動
python manage.py runserver
```

### 3. 訪問應用
- 應用主頁：http://localhost:8000
- 管理後台：http://localhost:8000/admin

## 📝 資料庫配置

- **資料庫名**: accounting_system
- **用戶**: postgres
- **密碼**: 見 `password.txt`
- **主機**: localhost
- **端口**: 5432

詳細資訊請查看 `DATABASE_README.md`

## 🔧 常用命令

```powershell
# 創建遷移
python manage.py makemigrations

# 執行遷移
python manage.py migrate

# 創建超級用戶
python manage.py createsuperuser

# 運行測試
python manage.py test

# 收集靜態文件
python manage.py collectstatic

# 進入 Django Shell
python manage.py shell
```

## 📦 已安裝套件

- Django 4.2.27
- psycopg2-binary (PostgreSQL 驅動)
- djangorestframework (REST API)
- django-cors-headers (CORS 支援)
- python-decouple (環境變數管理)

## 🎨 功能模組（待開發）

- [ ] 會計科目管理
- [ ] 會計分錄
- [ ] 總帳
- [ ] 財務報表
- [ ] 用戶管理
- [ ] 權限管理

## 📚 相關文檔

- [Django 官方文檔](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL 文檔](https://www.postgresql.org/docs/)

## 🔐 安全注意事項

⚠️ 當前配置為開發環境，部署到生產環境前請：

1. 修改 `SECRET_KEY`
2. 將 `DEBUG` 設為 `False`
3. 配置 `ALLOWED_HOSTS`
4. 使用環境變數存儲敏感資訊
5. 啟用 HTTPS
6. 配置資料庫備份

## 📧 支援

如有問題，請查閱：
- `SETUP_GUIDE.md` - 詳細設置指南
- `DATABASE_README.md` - 資料庫配置說明

---

**版本**: 1.0.0  
**最後更新**: 2025-12-30
