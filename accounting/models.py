from django.db import models
from django.utils import timezone

class Account(models.Model):
    """
    會計科目表 (Chart of Accounts)
    """
    TYPE_CHOICES = [
        ('ASSET', '資產'),
        ('LIABILITY', '負債'),
        ('EQUITY', '權益'),
        ('REVENUE', '收入'),
        ('EXPENSE', '費用'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="科目代碼")
    name = models.CharField(max_length=100, verbose_name="科目名稱")
    account_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="科目類別")
    is_control = models.BooleanField(default=False, verbose_name="統制帳戶")
    description = models.TextField(blank=True, null=True, verbose_name="科目說明")

    class Meta:
        db_table = 'accounts_account'  # 使用現有的資料庫表格
        verbose_name = "會計科目"
        verbose_name_plural = "會計科目列表"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} {self.name}"


class JournalEntry(models.Model):
    """
    傳票主檔 (Header)：代表「一張」傳票
    """
    date = models.DateField(default=timezone.now, verbose_name="傳票日期")
    description = models.CharField(max_length=255, verbose_name="傳票摘要")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後修改")

    # 未來可以加入: posted (是否過帳), created_by (建立者)

    class Meta:
        db_table = 'accounts_journalentry'  # 使用現有的資料庫表格
        verbose_name = "傳票主檔"
        verbose_name_plural = "傳票列表"
        ordering = ['-date', '-id'] # 預設顯示最新的

    def __str__(self):
        return f"{self.date} - {self.description[:20]}"


class JournalItem(models.Model):
    """
    傳票明細 (Line Items)：代表傳票裡的「借方」或「貸方」分錄
    """
    # on_delete=models.CASCADE 代表：如果刪除這張傳票(Entry)，底下的明細(Item)也會一起消失，這符合會計邏輯
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='items', verbose_name="所屬傳票")
    
    # on_delete=models.PROTECT 代表：如果有傳票用到了這個科目，就不允許刪除該科目（資料保護）
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="會計科目")
    
    description = models.CharField(max_length=255, blank=True, verbose_name="明細摘要")
    
    # 【關鍵】金額一定要用 Decimal，絕對不能用 Float (會有浮點數誤差)
    # max_digits=20, decimal_places=2 代表最大支援到 10^18 (百京)，小數點下兩位
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="借方金額")
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="貸方金額")

    class Meta:
        db_table = 'accounts_journalitem'  # 使用現有的資料庫表格
        verbose_name = "傳票明細"
        verbose_name_plural = "傳票明細"

    def __str__(self):
        return f"{self.account.name} (借:{self.debit} / 貸:{self.credit})"