from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    class Roles(models.TextChoices): ADMIN='ADMIN','Admin'; EMPLOYEE='EMPLOYEE','Employee'
    role=models.CharField(max_length=10,choices=Roles.choices,default=Roles.EMPLOYEE)
    employee_code=models.CharField(max_length=30,blank=True)
    def is_admin_user(self): return self.is_superuser or self.role==self.Roles.ADMIN
