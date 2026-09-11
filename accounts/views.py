from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeCreationForm
from .models import User
from audit.services import record
from django.db import transaction

class AppLoginView(LoginView):
    template_name = 'registration/login.html'
    from .forms import RoleAuthenticationForm
    authentication_form = RoleAuthenticationForm
    def form_valid(self, form):
        response = super().form_valid(form)
        record(form.get_user(), 'LOGIN', 'User', form.get_user().pk)
        return response

def staff_required(view):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'You do not have permission to access that page.')
            return redirect('dashboard')
        return view(request, *args, **kwargs)
    return wrapped

@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        login(request, request.user)
        messages.success(request, 'Password updated successfully.')
        return redirect('dashboard')
    return render(request, 'accounts/password.html', {'form': form})

@staff_required
def employees(request):
    return render(request, 'accounts/employees.html', {'employees': User.objects.filter(role=User.Roles.EMPLOYEE).order_by('first_name', 'username')})

@staff_required
def employee_create(request):
    form = EmployeeCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = User.Roles.EMPLOYEE
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        with transaction.atomic():
            user.save()
            record(request.user, 'EMPLOYEE_CREATED', 'User', user.pk, {'username': user.username})
        messages.success(request, 'Employee created successfully.')
        return redirect('employees')
    return render(request, 'accounts/employee_form.html', {'form': form})

@staff_required
def employee_toggle(request, pk):
    user = get_object_or_404(User, pk=pk, role=User.Roles.EMPLOYEE)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    record(request.user, 'EMPLOYEE_STATUS_CHANGED', 'User', pk, {'is_active': user.is_active})
    return redirect('employees')
