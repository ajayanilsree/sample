from .models import AuditLog
def record(user,action,entity_type,object_id='',metadata=None):
    return AuditLog.objects.create(user=user if getattr(user,'is_authenticated',False) else None,action=action,entity_type=entity_type,object_id=str(object_id),metadata=metadata or {})
