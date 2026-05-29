import uuid
from django.db import models

class Donation(models.Model):
    STATUS = [('RESERVED','Reserved'),('CONFIRMED','Confirmed'),('RELEASED','Released')]
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor_user_id = models.UUIDField()
    request_id    = models.UUIDField(null=True, blank=True)
    amount        = models.DecimalField(max_digits=10, decimal_places=2)
    status        = models.CharField(max_length=20, choices=STATUS, default='CONFIRMED')
    donated_at    = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'donations'
    def __str__(self): return f"Donation {self.amount} by {self.donor_user_id}"
