from decimal import Decimal
from django.db.models import Sum, Q

def totals(qs):
    values = qs.aggregate(income=Sum('amount', filter=Q(transaction_type='INCOME')), expense=Sum('amount', filter=Q(transaction_type='EXPENSE')))
    income, expense = values['income'] or Decimal('0.00'), values['expense'] or Decimal('0.00')
    return {'income': income, 'expense': expense, 'net': income - expense}
