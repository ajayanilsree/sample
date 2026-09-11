import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.views import staff_required
from accounts.models import User
from audit.services import record
from .forms import TransactionForm
from .models import Category, Transaction
from .services import totals

def scoped(request):
    qs = Transaction.objects.filter(is_deleted=False).select_related('category', 'created_by')
    return qs if request.user.is_admin_user() else qs.filter(created_by=request.user)

def filtered(request, qs=None):
    qs = qs or scoped(request)
    q, kind, category, payment = request.GET.get('q','').strip(), request.GET.get('type'), request.GET.get('category'), request.GET.get('payment')
    if q: qs = qs.filter(Q(description__icontains=q) | Q(reference__icontains=q) | Q(category__name__icontains=q))
    if kind in ('INCOME','EXPENSE'): qs = qs.filter(transaction_type=kind)
    if category: qs = qs.filter(category_id=category)
    if payment: qs = qs.filter(payment_method=payment)
    if request.GET.get('date_from'): qs = qs.filter(transaction_date__gte=request.GET['date_from'])
    if request.GET.get('date_to'): qs = qs.filter(transaction_date__lte=request.GET['date_to'])
    if request.user.is_admin_user() and request.GET.get('employee'): qs = qs.filter(created_by_id=request.GET['employee'])
    return qs

@login_required
def dashboard(request):
    qs = filtered(request); all_qs = scoped(request); today = timezone.localdate()
    return render(request, 'accounting/dashboard.html', {'summary': totals(qs), 'count': qs.count(), 'today': totals(all_qs.filter(transaction_date=today)), 'recent': qs[:8]})

@login_required
def transactions(request):
    page = Paginator(filtered(request), 15).get_page(request.GET.get('page'))
    return render(request, 'accounting/transactions.html', {'page': page, 'categories': Category.objects.filter(active=True), 'employees': User.objects.filter(role='EMPLOYEE') if request.user.is_admin_user() else [], 'payment_methods': Transaction.PaymentMethods.choices})

@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False); obj.created_by = request.user; obj.save(); record(request.user, 'TRANSACTION_CREATED', 'Transaction', obj.pk, {'amount': str(obj.amount), 'type': obj.transaction_type}); messages.success(request, 'Transaction saved.'); return redirect('transactions')
    return render(request, 'accounting/transaction_form.html', {'form': form, 'title': 'Add transaction'})

@login_required
def transaction_edit(request, pk):
    obj = get_object_or_404(scoped(request), pk=pk); form = TransactionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False); obj.updated_by = request.user; obj.save(); record(request.user, 'TRANSACTION_EDITED', 'Transaction', pk); messages.success(request, 'Transaction updated.'); return redirect('transactions')
    return render(request, 'accounting/transaction_form.html', {'form': form, 'title': 'Edit transaction'})

@login_required
def transaction_delete(request, pk):
    obj = get_object_or_404(scoped(request), pk=pk)
    if request.method == 'POST':
        obj.is_deleted, obj.deleted_at, obj.deleted_by = True, timezone.now(), request.user; obj.save(update_fields=['is_deleted','deleted_at','deleted_by']); record(request.user, 'TRANSACTION_DELETED', 'Transaction', pk); messages.success(request, 'Transaction moved to the audit history.'); return redirect('transactions')
    return render(request, 'accounting/confirm_delete.html', {'object': obj})

@login_required
def reports(request):
    qs = filtered(request)
    return render(request, 'accounting/reports.html', {'summary': totals(qs), 'transactions': qs, 'categories': Category.objects.filter(active=True), 'employees': User.objects.filter(role='EMPLOYEE') if request.user.is_admin_user() else [], 'payment_methods': Transaction.PaymentMethods.choices})

@staff_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv'); response['Content-Disposition'] = 'attachment; filename="transactions.csv"'; writer = csv.writer(response); writer.writerow(['Date','Type','Category','Amount','Payment method','Reference','Description','Created by'])
    for t in filtered(request): writer.writerow([t.transaction_date, t.get_transaction_type_display(), t.category.name, t.amount, t.get_payment_method_display(), t.reference, t.description, t.created_by.get_username()])
    return response

@staff_required
def transaction_restore(request, pk):
    obj = get_object_or_404(Transaction, pk=pk, is_deleted=True)
    if request.method == 'POST':
        obj.is_deleted = False; obj.deleted_at = None; obj.deleted_by = None; obj.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])
        record(request.user, 'TRANSACTION_RESTORED', 'Transaction', pk)
        messages.success(request, 'Transaction restored.')
    return redirect('transactions')
