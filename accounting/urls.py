from django.urls import path
from . import views

urlpatterns = [
    # 設定 dashboard 為根目錄 (空字串)
    path('', views.dashboard, name='dashboard'),
    path('entry/add/', views.entry_create, name='entry_create'),
    path('check-balance/', views.check_balance, name='check_balance'),
    # 新增日記帳和分類帳
    path('journal/', views.general_journal, name='general_journal'),
    path('ledger/', views.general_ledger, name='general_ledger'),
    # 財務報表
    path('reports/', views.financial_reports, name='financial_reports'),
]