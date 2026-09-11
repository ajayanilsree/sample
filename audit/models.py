from django.conf import settings
from django.db import models
class AuditLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    action=models.CharField(max_length=80); entity_type=models.CharField(max_length=80); object_id=models.CharField(max_length=80,blank=True); metadata=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta: ordering=['-created_at']
