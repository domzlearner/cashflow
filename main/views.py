
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm

class DashboardView(View):
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

        transactions = Transaction.objects.all().order_by('-date')[:10]
        
        context = {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'expense_categories': expense_categories,
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