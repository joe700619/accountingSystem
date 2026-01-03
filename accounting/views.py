from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import JournalEntry, JournalItem, Account
from .forms import JournalEntryForm, JournalEntryFormSet
from decimal import Decimal
from django.db.models import Sum

def entry_create(request):
    """建立新傳票的頁面"""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        formset = JournalEntryFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            # 1. 先儲存主檔 (但不寫入資料庫，因為要先拿到物件)
            entry = form.save()
            
            # 2. 把明細綁定到這個主檔上
            instances = formset.save(commit=False)
            for instance in instances:
                instance.entry = entry
                instance.save()
            
            # 3. 處理刪除的明細
            for obj in formset.deleted_objects:
                obj.delete()
                
            return redirect('/admin/') # 暫時先導回後台，之後改
            
    else:
        form = JournalEntryForm()
        formset = JournalEntryFormSet()

    return render(request, 'accounting/entry_create.html', {
        'form': form,
        'formset': formset
    })

def check_balance(request):
    """
    HTMX 專用：接收表單數據，計算借貸平衡，回傳 HTML 片段
    """
    # 從 POST 資料中抓取所有的 debit 和 credit
    total_debit = Decimal(0)
    total_credit = Decimal(0)
    
    # 解析 POST 資料 (這是比較髒的寫法，但為了教學簡單化)
    # Django formset 的欄位名稱通常是: items-0-debit, items-1-debit...
    for key, value in request.POST.items():
        if '-debit' in key and value:
            try: total_debit += Decimal(value)
            except: pass
        if '-credit' in key and value:
            try: total_credit += Decimal(value)
            except: pass

    balance = total_debit - total_credit
    is_balanced = balance == 0
    
    # 回傳一個小小的 HTML 片段給前端替換
    color = "text-green-600" if is_balanced else "text-red-600"
    status = "平衡" if is_balanced else f"差異: {balance}"
    
    html = f"""
    <div class="text-lg font-bold {color}">
        借方總計: {total_debit:,} | 貸方總計: {total_credit:,} | 狀態: {status}
    </div>
    """
    return HttpResponse(html)

def dashboard(request):
    """儀表板頁面"""
    # 撈出最近 5 筆傳票
    recent_entries = JournalEntry.objects.order_by('-date', '-created_at')[:5]
    return render(request, 'accounting/dashboard.html', {'recent_entries': recent_entries})

def general_journal(request):
    """日記帳：依照日期排列所有分錄"""
    entries = JournalEntry.objects.all().order_by('-date', '-id').prefetch_related('items__account')
    return render(request, 'accounting/general_journal.html', {'entries': entries})

def general_ledger(request):
    """分類帳：查詢特定科目的明細與餘額"""
    accounts = Account.objects.all()
    query_account_id = request.GET.get('account')
    ledger_items = []
    current_balance = 0
    selected_account = None
    selected_account_id = None  # 新增：用於模板比較

    if query_account_id:
        selected_account_id = int(query_account_id)  # 轉換為整數
        selected_account = Account.objects.get(id=query_account_id)
        items = JournalItem.objects.filter(account=selected_account).order_by('entry__date', 'id').select_related('entry')
        
        for item in items:
            if selected_account.account_type in ['ASSET', 'EXPENSE']:
                change = item.debit - item.credit
            else:
                change = item.credit - item.debit
                
            current_balance += change
            item.balance = current_balance
            ledger_items.append(item)

    return render(request, 'accounting/general_ledger.html', {
        'accounts': accounts,
        'selected_account': selected_account,
        'selected_account_id': selected_account_id,  # 新增：傳遞 ID
        'ledger_items': ledger_items,
    })

def financial_reports(request):
    """財務報表：資產負債表與損益表"""
    from datetime import date
    from django.db.models import Q
    
    # 從 GET 參數取得日期，預設為今天
    end_date = request.GET.get('end_date', date.today().strftime('%Y-%m-%d'))
    start_date = request.GET.get('start_date', date.today().replace(month=1, day=1).strftime('%Y-%m-%d'))
    
    # 取得所有科目
    accounts = Account.objects.all()
    
    # 計算各科目類別的餘額
    balances = {}
    totals = {
        'ASSET': Decimal(0),
        'LIABILITY': Decimal(0),
        'EQUITY': Decimal(0),
        'REVENUE': Decimal(0),
        'EXPENSE': Decimal(0),
    }
    
    for account in accounts:
        # 計算截止日期前的累計餘額
        items = JournalItem.objects.filter(
            account=account,
            entry__date__lte=end_date
        )
        
        total_debit = items.aggregate(Sum('debit'))['debit__sum'] or Decimal(0)
        total_credit = items.aggregate(Sum('credit'))['credit__sum'] or Decimal(0)
        
        # 根據科目類型計算餘額
        if account.account_type in ['ASSET', 'EXPENSE']:
            balance = total_debit - total_credit
        else:
            balance = total_credit - total_debit
        
        if balance != 0:  # 只顯示有餘額的科目
            if account.account_type not in balances:
                balances[account.account_type] = []
            balances[account.account_type].append({
                'account': account,
                'balance': balance
            })
            totals[account.account_type] += balance
    
    # 計算損益表期間的收入與費用
    income_items = []
    expense_items = []
    
    for account in accounts:
        items = JournalItem.objects.filter(
            account=account,
            entry__date__gte=start_date,
            entry__date__lte=end_date
        )
        
        total_debit = items.aggregate(Sum('debit'))['debit__sum'] or Decimal(0)
        total_credit = items.aggregate(Sum('credit'))['credit__sum'] or Decimal(0)
        
        if account.account_type == 'REVENUE':
            balance = total_credit - total_debit
            if balance != 0:
                income_items.append({'account': account, 'balance': balance})
        elif account.account_type == 'EXPENSE':
            balance = total_debit - total_credit
            if balance != 0:
                expense_items.append({'account': account, 'balance': balance})
    
    # 計算本期損益
    net_income = totals['REVENUE'] - totals['EXPENSE']
    
    # 權益加上本期損益
    total_equity_with_income = totals['EQUITY'] + net_income
    
    context = {
        'report': balances,  # 模板中使用 report.ASSET 等變量名
        'totals': totals,
        'income_items': income_items,
        'expense_items': expense_items,
        'net_income': net_income,
        'total_equity_with_income': total_equity_with_income,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'accounting/financial_reports.html', context)
