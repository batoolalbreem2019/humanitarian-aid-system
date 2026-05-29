import uuid
from django.db import models

class Distribution(models.Model):
    STATUS = [
        ('SCHEDULED','Scheduled'),('IN_PROGRESS','In Progress'),
        ('DELIVERED','Delivered'),('CANCELLED','Cancelled'),
    ]
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_id     = models.UUIDField()
    volunteer_id   = models.UUIDField(null=True, blank=True)
    scheduled_date = models.DateField()
    location       = models.CharField(max_length=300)
    status         = models.CharField(max_length=20, choices=STATUS, default='SCHEDULED')
    created_at     = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'distributions'
    def __str__(self): return f"Distribution for request {self.request_id}"
