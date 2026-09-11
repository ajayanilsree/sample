from django.urls import path
from .views import change_password, employees, employee_create, employee_toggle

urlpatterns = [
    path('password/', change_password, name='change_password'),
    path('employees/', employees, name='employees'),
    path('employees/new/', employee_create, name='employee_create'),
    path('employees/<int:pk>/toggle/', employee_toggle, name='employee_toggle'),
]
