from django import forms
from django.forms import inlineformset_factory
from .models import JournalEntry, JournalItem

class JournalEntryForm(forms.ModelForm):
    """傳票主檔表單"""
    class Meta:
        model = JournalEntry
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'description': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': '請輸入傳票摘要'}),
        }

class JournalItemForm(forms.ModelForm):
    """傳票明細表單 (每一行)"""
    class Meta:
        model = JournalItem
        fields = ['account', 'description', 'debit', 'credit']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-input'}),
            # 我們加入 hx-trigger，當數值改變時，觸發前端重新計算
            'debit': forms.NumberInput(attrs={'class': 'form-input text-right debit-input', 'hx-trigger': 'keyup changed delay:500ms', 'hx-post': '/accounting/check-balance/', 'hx-target': '#balance-status'}),
            'credit': forms.NumberInput(attrs={'class': 'form-input text-right credit-input', 'hx-trigger': 'keyup changed delay:500ms', 'hx-post': '/accounting/check-balance/', 'hx-target': '#balance-status'}),
        }

# 這就是魔法：建立一個能管理「主檔 vs 明細」的關聯表單集合
# extra=2 代表預設顯示 2 行空白明細
JournalEntryFormSet = inlineformset_factory(
    JournalEntry, JournalItem, form=JournalItemForm,
    extra=2, can_delete=True
)
