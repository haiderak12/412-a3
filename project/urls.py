# project/urls.py
# description: URL patterns for the budgeting app

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and Profile Creation
    path('', HomeView.as_view(), name='home'),
    path('create-profile/', ProfileCreateView.as_view(), name='profile_create'),
    
    # Custom Login/Logout
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Transactions
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),

    # Budgets
    path('budget-summary/', BudgetSummaryView.as_view(), name='budget_summary'),
    path('budget/add/', BudgetCreateView.as_view(), name='budget_add'),
    path('budget/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget_edit'),
    path('budget/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),

    # Recurring Transactions
    # Recurring transactions
    path('recurring/', RecurringTransactionListView.as_view(), name='recurring_list'),
    path('recurring/add/', RecurringTransactionCreateView.as_view(), name='recurring_add'),
    path('recurring/<int:pk>/edit/', RecurringTransactionUpdateView.as_view(), name='recurring_edit'),
    path('recurring/<int:pk>/delete/', RecurringTransactionDeleteView.as_view(), name='recurring_delete'),
]