from django.contrib import admin
from .models import Account, JournalEntry, JournalItem

# 這是一個進階設定：讓你在編輯「傳票主檔」時，可以直接在同一頁編輯「明細」
# 就像你在用會計軟體時，上面打日期，下面直接打借貸行
class JournalItemInline(admin.TabularInline):
    model = JournalItem
    extra = 2  # 預設顯示兩行空白 (一借一貸)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'account_type')
    search_fields = ('code', 'name')
    list_filter = ('account_type',)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'created_at')
    inlines = [JournalItemInline]  # 把明細嵌入進來

# JournalItem 不需要單獨註冊，因為它依附在 JournalEntry 底下
