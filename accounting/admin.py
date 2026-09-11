from django.contrib import admin
from .models import Category, Transaction
admin.site.register(Category)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=('transaction_date','transaction_type','category','amount','created_by','is_deleted')
    list_filter=('transaction_type','is_deleted','payment_method')
