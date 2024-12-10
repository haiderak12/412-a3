from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from django.db.models import Sum, Q
from .models import *
from .forms import *

import plotly.graph_objs as go
import plotly.offline as pyo
from django.utils import timezone
import datetime

# Home view (public/homepage)
class HomeView(TemplateView):
    """
    Display the public homepage for unauthenticated users.
    """
    template_name = 'project/home.html'

# Profile (User) creation view
class ProfileCreateView(CreateView):
    """
    Allow a new user to create a profile (register an account).
    """
    form_class = UserCreationForm
    template_name = 'project/profile_create.html'
    success_url = reverse_lazy('login')  # After successful creation, redirect to login page

# Custom login/logout views
def login_view(request):
    """
    Display the login page and authenticate the user upon form submission.
    """
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to dashboard or home
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Retrieve user object from form
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
    else:
        form = AuthenticationForm()
    
    return render(request, 'project/login.html', {'form': form})


def logout_view(request):
    """
    Log the user out and redirect them to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

class DashboardView(LoginRequiredMixin, View):
    """
    Display a dashboard with financial summaries, charts, and filtering by month and year.
    """
    def get(self, request):
        user = request.user
        # Calculate totals
        total_income = Transaction.objects.filter(user=user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Transaction.objects.filter(user=user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense

        # Get month/year from query params or default to current month/year
        now = timezone.now()
        month = request.GET.get('month')
        year = request.GET.get('year')
        if month is None:
            month = now.month
        else:
            month = int(month)
        if year is None:
            year = now.year
        else:
            year = int(year)

        # Calculate start and end of the chosen month
        start_date = datetime.datetime(year, month, 1)
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1)
        else:
            end_date = datetime.datetime(year, month + 1, 1)

        # Filter expenses for the chosen month
        monthly_expenses = Transaction.objects.filter(
            user=user,
            type='expense',
            date__gte=start_date,
            date__lt=end_date
        )

        # Aggregate by category
        category_data = (
            monthly_expenses.values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('category__name')
        )

        categories = [c['category__name'] if c['category__name'] else "Other" for c in category_data]
        values = [c['total'] for c in category_data]

        # Prepare figure HTML using Plotly
        if categories:
            fig = go.Figure(data=[go.Pie(labels=categories, values=values, hole=0)])
            # Generate the div containing the figure
            figure_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)
        else:
            figure_html = "<p>No Data</p>"

        # Provide options for month/year selection
        available_months = [
            (1, "January"), (2, "February"), (3, "March"), (4, "April"),
            (5, "May"), (6, "June"), (7, "July"), (8, "August"),
            (9, "September"), (10, "October"), (11, "November"), (12, "December")
        ]
        
        current_year = now.year
        available_years = [current_year, current_year - 1, current_year - 2]

        context = {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'figure_html': figure_html,
            'current_month': month,
            'current_year': year,
            'available_months': available_months,
            'available_years': available_years,
        }
        return render(request, 'project/dashboard.html', context)


### Transaction CRUD Views

class TransactionListView(LoginRequiredMixin, ListView):
    """
    Display a list of all the logged-in user's transactions.
    """
    model = Transaction
    template_name = 'project/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        """Return transactions belonging to the currently logged-in user, ordered by date."""
        return Transaction.objects.filter(user=self.request.user).order_by('-date')


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Provide a form to create a new transaction for the logged-in user.
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'project/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        """Automatically set the user on the new transaction before saving."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Provide a form to update an existing transaction owned by the logged-in user.
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'project/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        """Only allow editing transactions that belong to the current user."""
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allow the logged-in user to delete one of their transactions.
    """
    model = Transaction
    template_name = 'project/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        """Only allow deleting transactions that belong to the current user."""
        return Transaction.objects.filter(user=self.request.user)
    
### Budget CRUD Views

class BudgetSummaryView(LoginRequiredMixin, View):
    """
    Display a summary of all budgets for the logged-in user, including monthly usage progress.
    """
    def get(self, request):
        user = request.user
        now = timezone.now()

        # Get month/year from GET or default to current month/year
        month = request.GET.get('month')
        year = request.GET.get('year')

        if month is None:
            month = now.month
        else:
            month = int(month)

        if year is None:
            year = now.year
        else:
            year = int(year)

        # Calculate date range for the selected month
        start_date = datetime.datetime(year, month, 1)
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1)
        else:
            end_date = datetime.datetime(year, month + 1, 1)

        budgets = Budget.objects.filter(user=user).select_related('category')

        # Calculate monthly spending per category
        budget_data = []
        for b in budgets:
            total_spent = Transaction.objects.filter(
                user=user,
                type='expense',
                category=b.category,
                date__gte=start_date,
                date__lt=end_date
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Calculate percentage
            if b.monthly_limit > 0:
                percentage = (total_spent / b.monthly_limit) * 100
            else:
                percentage = 0

            # Determine the bar color and width
            if total_spent > b.monthly_limit:
                bar_color = 'red'
                bar_width = 100
            else:
                bar_color = 'green'
                bar_width = min(100, percentage)

            budget_data.append({
                'budget': b,
                'total_spent': total_spent,
                'percentage': percentage,
                'bar_color': bar_color,
                'bar_width': bar_width,
            })

        # Available months and years for the dropdown
        available_months = [
            (1, "January"), (2, "February"), (3, "March"), (4, "April"),
            (5, "May"), (6, "June"), (7, "July"), (8, "August"),
            (9, "September"), (10, "October"), (11, "November"), (12, "December")
        ]
        current_year = now.year
        available_years = [current_year, current_year - 1, current_year - 2]

        # Calculate total monthly budget
        total_monthly_budget = budgets.aggregate(Sum('monthly_limit'))['monthly_limit__sum'] or 0

        context = {
            'budgets': budget_data,
            'total_monthly_budget': total_monthly_budget,
            'current_month': month,
            'current_year': year,
            'available_months': available_months,
            'available_years': available_years,
        }
        
        return render(request, 'project/budget_summary.html', context)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    """
    Allow the user to create a new budget tied to a selected category.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'project/budget_form.html'
    success_url = reverse_lazy('budget_summary')

    def form_valid(self, form):
        """Set the current user on the newly created budget."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        """Customize the form to display all available categories for selection."""
        form = super().get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.all()
        return form


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    """
    Provide a form to update an existing budget's monthly limit.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'project/budget_form.html'
    success_url = reverse_lazy('budget_summary')

    def get_queryset(self):
        """Only allow editing budgets that belong to the current user."""
        return Budget.objects.filter(user=self.request.user)

    def get_form(self, *args, **kwargs):
        """Allow changing the monthly limit but keep category choices global."""
        form = super().get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.all()
        return form


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allow the user to delete one of their budgets.
    """
    model = Budget
    template_name = 'project/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_summary')

    def get_queryset(self):
        """Only allow deleting budgets that belong to the current user."""
        return Budget.objects.filter(user=self.request.user)
    
### Recurring Transactions CRUD Views

class RecurringTransactionListView(LoginRequiredMixin, ListView):
    """
    Display a list of all the user's recurring transactions.
    """
    model = RecurringTransaction
    template_name = 'project/recurring_list.html'
    context_object_name = 'recurring_transactions'

    def get_queryset(self):
        """Return recurring transactions belonging to the current user."""
        return RecurringTransaction.objects.filter(user=self.request.user).order_by('start_date')

class RecurringTransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Allow the user to create a new recurring transaction.
    """
    model = RecurringTransaction
    form_class = RecurringTransactionForm
    template_name = 'project/recurring_form.html'
    success_url = reverse_lazy('recurring_list')

    def form_valid(self, form):
        """Set the current user on the new recurring transaction."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        """Display all categories for the user to choose from."""
        form = super().get_form(*args, **kwargs)
        form.fields['category'].queryset = form.fields['category'].queryset.all()
        return form

class RecurringTransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Provide a form to update an existing recurring transaction.
    """
    model = RecurringTransaction
    form_class = RecurringTransactionForm
    template_name = 'project/recurring_form.html'
    success_url = reverse_lazy('recurring_list')

    def get_queryset(self):
        """Only allow updating recurring transactions that belong to the current user."""
        return RecurringTransaction.objects.filter(user=self.request.user)

    def get_form(self, *args, **kwargs):
        """Allow editing recurring transaction details and choose from all categories."""
        form = super().get_form(*args, **kwargs)
        form.fields['category'].queryset = form.fields['category'].queryset.all()
        return form

class RecurringTransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allow the user to delete one of their recurring transactions.
    """
    model = RecurringTransaction
    template_name = 'project/recurring_confirm_delete.html'
    success_url = reverse_lazy('recurring_list')

    def get_queryset(self):
        """Only allow deleting recurring transactions that belong to the current user."""
        return RecurringTransaction.objects.filter(user=self.request.user)
