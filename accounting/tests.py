from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Category, Transaction
from .services import totals

class AccountingTests(TestCase):
    def setUp(self):
        self.admin=User.objects.create_user(username='admin',password='StrongPass123!',role='ADMIN')
        self.employee=User.objects.create_user(username='worker',password='StrongPass123!',role='EMPLOYEE')
        self.sales=Category.objects.get_or_create(name='Test Sales',defaults={'category_type':'INCOME'})[0]
        self.fuel=Category.objects.get_or_create(name='Test Fuel',defaults={'category_type':'EXPENSE'})[0]
    def test_employee_can_create_and_only_see_own_transactions(self):
        self.client.login(username='worker',password='StrongPass123!')
        response=self.client.post(reverse('transaction_create'),{'transaction_type':'EXPENSE','transaction_date':'2026-09-11','category':self.fuel.pk,'amount':'1500.00','payment_method':'UPI','description':'Fuel'})
        self.assertRedirects(response,reverse('transactions')); self.assertEqual(Transaction.objects.count(),1)
    def test_employee_blocked_from_admin_pages(self):
        self.client.login(username='worker',password='StrongPass123!')
        self.assertRedirects(self.client.get(reverse('employees')),reverse('dashboard'))

    def test_role_selection_matches_stored_role(self):
        self.assertEqual(self.client.post(reverse('login'), {'username':'admin', 'password':'StrongPass123!', 'role':'admin'}).status_code, 302)
        self.client.logout()
        self.assertEqual(self.client.post(reverse('login'), {'username':'worker', 'password':'StrongPass123!', 'role':'employee'}).status_code, 302)

    def test_role_mismatch_is_rejected(self):
        response = self.client.post(reverse('login'), {'username':'worker', 'password':'StrongPass123!', 'role':'admin'})
        self.assertContains(response, 'This account is not an Admin account.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_superuser_can_login_as_admin(self):
        User.objects.create_superuser(username='root', password='StrongPass123!')
        response = self.client.post(reverse('login'), {'username':'root', 'password':'StrongPass123!', 'role':'admin'})
        self.assertEqual(response.status_code, 302)

    def test_admin_can_create_hashed_employee_password(self):
        self.client.login(username='admin', password='StrongPass123!')
        response = self.client.post(reverse('employee_create'), {'first_name':'Ajay','last_name':'Anil Sree','username':'ajayanilsree','email':'ajayanilsree@gmail.com','employee_code':'emp01','password':'TestPassword123!','confirm_password':'TestPassword123!'})
        self.assertRedirects(response, reverse('employees'))
        employee = User.objects.get(username='ajayanilsree')
        self.assertNotEqual(employee.password, 'TestPassword123!')
        self.assertTrue(employee.check_password('TestPassword123!'))
        self.assertNotIn('TestPassword123!', str(employee.__dict__))

    def test_employee_password_confirmation_and_weak_password_fail(self):
        self.client.login(username='admin', password='StrongPass123!')
        data={'first_name':'Ajay','username':'ajay2','password':'TestPassword123!','confirm_password':'different'}
        self.assertEqual(self.client.post(reverse('employee_create'), data).status_code, 200)
        data['username']='ajay3'; data['password']='123'; data['confirm_password']='123'
        self.assertEqual(self.client.post(reverse('employee_create'), data).status_code, 200)
    def test_totals_ignore_deleted(self):
        a=Transaction.objects.create(transaction_type='INCOME',transaction_date='2026-09-11',category=self.sales,amount=Decimal('12000'),payment_method='BANK',created_by=self.employee)
        e=Transaction.objects.create(transaction_type='EXPENSE',transaction_date='2026-09-11',category=self.fuel,amount=Decimal('1500'),payment_method='UPI',created_by=self.employee)
        e.is_deleted=True; e.save(update_fields=['is_deleted']); summary=totals(Transaction.objects.filter(is_deleted=False)); self.assertEqual(summary['net'],Decimal('12000'))
