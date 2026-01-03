import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=== 測試 imports ===")
try:
    from accounting.models import JournalEntry, JournalItem
    print("✅ Models imported successfully")
except Exception as e:
    print(f"❌ Models import error: {e}")

try:
    from accounting.forms import JournalEntryForm, JournalEntryFormSet
    print("✅ Forms imported successfully")
except Exception as e:
    print(f"❌ Forms import error: {e}")

try:
    from accounting.views import entry_create, check_balance
    print("✅ Views imported successfully")
except Exception as e:
    print(f"❌ Views import error: {e}")

print("\n=== 測試 URL patterns ===")
try:
    from django.urls import reverse
    print(f"✅ URL 'entry_create': {reverse('entry_create')}")
except Exception as e:
    print(f"❌ URL reverse error: {e}")

print("\n所有測試完成！")
