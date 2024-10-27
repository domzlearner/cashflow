
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
import json
from decimal import Decimal

class DashboardView(LoginRequiredMixin, View):
    login_url = '/account/signin/'
    redirect_field_name = 'next'

    def get(self, request):
        income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expenses

        expense_categories = {
            'bills': Transaction.objects.filter(transaction_type='expense', expense_category='bills').aggregate(Sum('amount'))['amount__sum'] or 0,
            'savings': Transaction.objects.filter(transaction_type='expense', expense_category='savings').aggregate(Sum('amount'))['amount__sum'] or 0,
            'debts': Transaction.objects.filter(transaction_type='expense', expense_category='debts').aggregate(Sum('amount'))['amount__sum'] or 0,
            'others': Transaction.objects.filter(transaction_type='expense', expense_category='others').aggregate(Sum('amount'))['amount__sum'] or 0,
        }

        # Income breakdown
        income_breakdown = list(Transaction.objects.filter(transaction_type='income')
                                .values('description')
                                .annotate(total=Sum('amount'))
                                .order_by('-total'))

        # Expense categories breakdown
        expense_categories = list(Transaction.objects.filter(transaction_type='expense')
                                  .values('expense_category')
                                  .annotate(total=Sum('amount'))
                                  .order_by('-total'))

        # Income vs Expense breakdown
        income_vs_expense = [
            {'name': 'Income', 'value': float(income)},
            {'name': 'Expense', 'value': float(expenses)},
        ]

        transactions = Transaction.objects.all().order_by('-date')[:10]
        
        # Convert Decimal to float for JSON serialization
        for item in income_breakdown + expense_categories:
            item['total'] = float(item['total'])

        context = {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'income_breakdown': json.dumps(income_breakdown),
            'expense_categories': json.dumps(expense_categories),
            'income_vs_expense': json.dumps(income_vs_expense),
            'transactions': transactions,
        }
        return render(request, 'main/dashboard.html', context)

class TransactionListView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by('-date')
        return render(request, 'main/transaction_list.html', {'transactions': transactions})

class TransactionCreateView(View):
    def get(self, request):
        form = TransactionForm()
        return render(request, 'main/transaction_form.html', {'form': form})

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
        return render(request, 'main/transaction_form.html', {'form': form})
    
class TransactionUpdateView(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        form = TransactionForm(instance=transaction)
        return render(request, 'main/transaction_form.html', {'form': form, 'transaction': transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
        return render(request, 'main/transaction_form.html', {'form': form, 'transaction': transaction})

class TransactionDeleteView(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        return render(request, 'main/transaction_confirm_delete.html', {'transaction': transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return redirect('transaction_list')