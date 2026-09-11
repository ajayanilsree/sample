from django.shortcuts import render
from accounts.views import staff_required
from .models import AuditLog

@staff_required
def audit_list(request):
    return render(request, 'audit/list.html', {'logs': AuditLog.objects.select_related('user')[:200]})
