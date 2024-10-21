
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.transaction_type.capitalize()}: {self.amount} - {self.description}"