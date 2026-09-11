from django.urls import path
from . import views
from audit.views import audit_list

urlpatterns = [
    path('', views.dashboard, name='dashboard'), path('transactions/', views.transactions, name='transactions'), path('transactions/new/', views.transaction_create, name='transaction_create'), path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'), path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'), path('transactions/<int:pk>/restore/', views.transaction_restore, name='transaction_restore'), path('reports/', views.reports, name='reports'), path('reports/export.csv', views.export_csv, name='export_csv'), path('audit/', audit_list, name='audit_list'),
]
