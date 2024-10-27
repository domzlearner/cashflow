from django.urls import path
from .views import DashboardView, TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('tx/', TransactionListView.as_view(), name='transaction_list'),
    path('tx/add/', TransactionCreateView.as_view(), name='transaction_create'),
    path('tx/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('tx/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]