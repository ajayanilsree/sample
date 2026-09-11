from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'transaction_date', 'category', 'amount', 'payment_method', 'reference', 'description']
        widgets = {'transaction_date': forms.DateInput(attrs={'type': 'date'}), 'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'inputmode': 'decimal'}), 'description': forms.Textarea(attrs={'rows': 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(active=True)
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0: raise ValidationError('Amount must be greater than zero.')
        return amount
    def clean(self):
        data = super().clean()
        category, kind = data.get('category'), data.get('transaction_type')
        if category and kind and category.category_type not in (kind, Category.Types.BOTH): self.add_error('category', 'Choose a category that matches the transaction type.')
        return data
