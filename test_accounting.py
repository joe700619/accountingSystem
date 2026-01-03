import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounting.models import Account, JournalEntry, JournalItem

print("=== 檢查資料庫資料 ===\n")

# 檢查會計科目
accounts = Account.objects.all()
print(f"會計科目數量: {accounts.count()}")
if accounts.exists():
    print("前 5 筆會計科目:")
    for acc in accounts[:5]:
        print(f"  - {acc.code} {acc.name}")
else:
    print("⚠️ 警告：資料庫中沒有會計科目！")
    print("   您需要先在 Admin 後台建立會計科目，才能新增傳票。")

print(f"\n傳票數量: {JournalEntry.objects.count()}")
print(f"傳票明細數量: {JournalItem.objects.count()}")

print("\n=== URL 測試 ===")
from django.urls import reverse
try:
    url = reverse('entry_create')
    print(f"✅ entry_create URL: http://127.0.0.1:8000{url}")
except Exception as e:
    print(f"❌ URL error: {e}")
