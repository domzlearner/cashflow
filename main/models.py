
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    EXPENSE_CATEGORIES = (
        ('bills', 'Bills'),
        ('savings', 'Savings'),
        ('debts', 'Debts'),
        ('others', 'Others'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    expense_category = models.CharField(max_length=7, choices=EXPENSE_CATEGORIES, null=True, blank=True)

    def __str__(self):
        if self.transaction_type == 'expense':
            return f"Expense ({self.expense_category}): {self.amount} - {self.description}"
        return f"{self.transaction_type.capitalize()}: {self.amount} - {self.description}"