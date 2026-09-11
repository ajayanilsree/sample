from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model('accounting', 'Category')
    for name, kind in [('Sales','INCOME'), ('Service Income','INCOME'), ('Customer Payment','INCOME'), ('Other Income','INCOME'), ('Purchase','EXPENSE'), ('Salary','EXPENSE'), ('Fuel','EXPENSE'), ('Travel','EXPENSE'), ('Food','EXPENSE'), ('Office Expense','EXPENSE'), ('Utilities','EXPENSE'), ('Maintenance','EXPENSE'), ('Other Expense','EXPENSE')]:
        Category.objects.get_or_create(name=name, defaults={'category_type': kind, 'active': True})

class Migration(migrations.Migration):
    dependencies = [('accounting', '0001_initial')]
    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
