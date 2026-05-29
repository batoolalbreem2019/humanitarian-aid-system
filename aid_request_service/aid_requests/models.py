import uuid
from django.db import models

class AidRequest(models.Model):
    STATUS = [
        ('PENDING','Pending'),('APPROVED','Approved'),
        ('DISPATCHED','Dispatched'),('DELIVERED','Delivered'),('CANCELLED','Cancelled'),
    ]
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id      = models.UUIDField()
    request_type = models.CharField(max_length=100)
    description  = models.TextField()
    status       = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    created_at   = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'aid_requests'
    def __str__(self): return f"Request {self.id} ({self.status})"
