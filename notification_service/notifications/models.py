import uuid
from django.db import models

class Notification(models.Model):
    TYPE_CHOICES = [
        ('AID_APPROVED','Aid Approved'),
        ('AID_DELIVERED','Aid Delivered'),
        ('DONATION_RECEIVED','Donation Received'),
        ('AID_CANCELLED','Aid Cancelled'),
    ]
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id     = models.UUIDField()
    request_id  = models.UUIDField(null=True, blank=True)
    type        = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message     = models.TextField()
    sent_at     = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'notifications'
