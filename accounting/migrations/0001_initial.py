from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.CreateModel(name='Category', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80, unique=True)), ('category_type', models.CharField(choices=[('INCOME','Income'),('EXPENSE','Expense'),('BOTH','Both')], default='BOTH', max_length=8)), ('active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name='Transaction', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('transaction_type', models.CharField(choices=[('INCOME','Income'),('EXPENSE','Expense')], db_index=True, max_length=7)), ('transaction_date', models.DateField(db_index=True)), ('amount', models.DecimalField(decimal_places=2, max_digits=12)), ('payment_method', models.CharField(choices=[('CASH','Cash'),('UPI','UPI'),('BANK','Bank Transfer'),('CARD','Card'),('OTHER','Other')], max_length=10)), ('reference', models.CharField(blank=True, max_length=100)), ('description', models.TextField(blank=True)), ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)), ('updated_at', models.DateTimeField(auto_now=True)), ('is_deleted', models.BooleanField(db_index=True, default=False)), ('deleted_at', models.DateTimeField(blank=True, null=True)), ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.category')), ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_transactions', to=settings.AUTH_USER_MODEL)), ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_transactions', to=settings.AUTH_USER_MODEL)), ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_transactions', to=settings.AUTH_USER_MODEL))]),
        migrations.AddIndex(model_name='transaction', index=models.Index(fields=['transaction_date','is_deleted'], name='accounting__transac_1d4d9e_idx')),
        migrations.AddIndex(model_name='transaction', index=models.Index(fields=['created_by','is_deleted'], name='accounting__created_4b9a84_idx')),
    ]
