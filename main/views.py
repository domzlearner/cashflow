
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm

class DashboardView(View):
    def get(self, request):
        income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expenses
        transactions = Transaction.objects.all().order_by('-date')[:10]
        
        context = {
            'income': income,
            'expenses': expenses,
            'balance': balance,
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