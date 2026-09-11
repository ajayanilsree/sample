from django.conf import settings
from django.db import models
class Category(models.Model):
    class Types(models.TextChoices): INCOME='INCOME','Income'; EXPENSE='EXPENSE','Expense'; BOTH='BOTH','Both'
    name=models.CharField(max_length=80,unique=True); category_type=models.CharField(max_length=8,choices=Types.choices,default=Types.BOTH); active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Transaction(models.Model):
    class Types(models.TextChoices): INCOME='INCOME','Income'; EXPENSE='EXPENSE','Expense'
    class PaymentMethods(models.TextChoices): CASH='CASH','Cash'; UPI='UPI','UPI'; BANK='BANK','Bank Transfer'; CARD='CARD','Card'; OTHER='OTHER','Other'
    transaction_type=models.CharField(max_length=7,choices=Types.choices,db_index=True); transaction_date=models.DateField(db_index=True); category=models.ForeignKey(Category,on_delete=models.PROTECT); amount=models.DecimalField(max_digits=12,decimal_places=2); payment_method=models.CharField(max_length=10,choices=PaymentMethods.choices); reference=models.CharField(max_length=100,blank=True); description=models.TextField(blank=True); created_by=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='created_transactions',on_delete=models.PROTECT); updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='updated_transactions',null=True,blank=True,on_delete=models.PROTECT); created_at=models.DateTimeField(auto_now_add=True,db_index=True); updated_at=models.DateTimeField(auto_now=True); is_deleted=models.BooleanField(default=False,db_index=True); deleted_at=models.DateTimeField(null=True,blank=True); deleted_by=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='deleted_transactions',null=True,blank=True,on_delete=models.PROTECT)
    class Meta:
        indexes=[models.Index(fields=['transaction_date','is_deleted']),models.Index(fields=['created_by','is_deleted'])]; ordering=['-transaction_date','-created_at']
