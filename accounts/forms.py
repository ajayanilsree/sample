from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from .models import User

class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), strip=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), strip=False, label='Confirm password')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'employee_code']
    def clean(self):
        cleaned = super().clean()
        password, confirmation = cleaned.get('password'), cleaned.get('confirm_password')
        if password and confirmation and password != confirmation:
            self.add_error('confirm_password', 'Passwords do not match.')
        if password:
            validate_password(password, self.instance)
        return cleaned

class RoleAuthenticationForm(AuthenticationForm):
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('employee', 'Employee')], widget=forms.RadioSelect, required=True)
    def clean(self):
        cleaned = super().clean()
        user, selected = self.get_user(), cleaned.get('role')
        if user and selected:
            is_admin = user.is_admin_user()
            is_employee = user.role == User.Roles.EMPLOYEE and not user.is_superuser
            if (selected == 'admin' and not is_admin) or (selected == 'employee' and not is_employee):
                label = 'Admin' if selected == 'admin' else 'Employee'
                raise forms.ValidationError(f'This account is not an {label} account.')
        return cleaned

class ForcePasswordChangeForm(SetPasswordForm):
    pass
