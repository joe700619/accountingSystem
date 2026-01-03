import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounting.models import Account, JournalEntry, JournalItem

print("=" * 60)
print("資料庫資料檢查")
print("=" * 60)

# 檢查會計科目
accounts = Account.objects.all()
print(f"\n【會計科目】數量: {accounts.count()}")
if accounts.exists():
    for acc in accounts:
        print(f"  - {acc.code} {acc.name} ({acc.get_account_type_display()})")

# 檢查傳票主檔
entries = JournalEntry.objects.all().order_by('-date', '-created_at')
print(f"\n【傳票主檔】數量: {entries.count()}")
if entries.exists():
    for entry in entries:
        print(f"\n  傳票 #{entry.id}")
        print(f"    日期: {entry.date}")
        print(f"    摘要: {entry.description}")
        print(f"    建立時間: {entry.created_at}")
        
        # 顯示該傳票的明細
        items = entry.items.all()
        print(f"    明細數量: {items.count()}")
        total_debit = 0
        total_credit = 0
        for item in items:
            print(f"      - {item.account.name}: 借 {item.debit} / 貸 {item.credit}")
            total_debit += item.debit
            total_credit += item.credit
        print(f"    合計: 借方 {total_debit} / 貸方 {total_credit}")
        print(f"    平衡: {'✓ 是' if total_debit == total_credit else '✗ 否'}")
else:
    print("  >> 目前沒有傳票資料")

# 檢查傳票明細
items = JournalItem.objects.all()
print(f"\n【傳票明細】數量: {items.count()}")

print("\n" + "=" * 60)
