# 會計系統資料庫配置資訊

## 資料庫詳情
- **資料庫名稱**: accounting_system
- **使用者**: postgres
- **密碼**: 5201314Aa
- **主機**: localhost
- **端口**: 5432
- **編碼**: UTF8

## Django Settings.py 配置

請在您的 Django 專案的 `settings.py` 文件中加入以下配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'accounting_system',
        'USER': 'postgres',
        'PASSWORD': '5201314Aa',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 所需的 Python 套件

確保已安裝 PostgreSQL 的 Python 驅動程式：

```bash
pip install psycopg2-binary
```

或者（推薦用於生產環境）：

```bash
pip install psycopg2
```

## 下一步操作

1. **安裝 psycopg2**:
   ```bash
   pip install psycopg2-binary
   ```

2. **配置 Django settings.py**:
   按照上面的配置更新您的 Django 設定檔

3. **執行資料庫遷移**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **創建超級使用者**:
   ```bash
   python manage.py createsuperuser
   ```

## 常用命令

### 連接到資料庫（命令列）
```powershell
$env:PGPASSWORD = "5201314Aa"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d accounting_system
```

### 列出所有資料表
```sql
\dt
```

### 查看資料庫資訊
```sql
\l
```

### 退出 psql
```sql
\q
```

## 備份與還原

### 備份資料庫
```powershell
$env:PGPASSWORD = "5201314Aa"
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U postgres -d accounting_system -f backup.sql
```

### 還原資料庫
```powershell
$env:PGPASSWORD = "5201314Aa"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d accounting_system -f backup.sql
```
