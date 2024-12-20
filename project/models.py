from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    A category for organizing transactions, shared globally among all users.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    A single user-owned financial transaction, either income or expense, associated with a category.
    """
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.title} ({self.type}) - ${self.amount}"


class Budget(models.Model):
    """
    A monthly spending limit set by a user for a specific category.
    """
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='budget')
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')

    def __str__(self):
        return f"{self.category.name} - ${self.monthly_limit}"


class RecurringTransaction(models.Model):
    """
    A user-defined transaction that repeats on a specified frequency (daily, weekly, monthly, or yearly).
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='recurring_transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_transactions')

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.frequency})"