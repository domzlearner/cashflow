
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'date', 'transaction_type', 'expense_category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_category'].widget = forms.Select(choices=Transaction.EXPENSE_CATEGORIES)
        self.fields['expense_category'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        expense_category = cleaned_data.get('expense_category')

        if transaction_type == 'expense' and not expense_category:
            raise forms.ValidationError("Expense category is required for expenses.")
        elif transaction_type == 'income' and expense_category:
            cleaned_data['expense_category'] = None

        return cleaned_data