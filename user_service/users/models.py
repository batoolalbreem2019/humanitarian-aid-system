import uuid
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('BENEFICIARY','Beneficiary'),('VOLUNTEER','Volunteer'),
        ('DONOR','Donor'),('ADMIN','Admin'),
    ]
    STATUS_CHOICES = [
        ('PENDING','Pending'),('ACTIVE','Active'),('SUSPENDED','Suspended'),
    ]
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email     = models.EmailField(unique=True)
    phone     = models.CharField(max_length=20)
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location  = models.CharField(max_length=200)
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    password  = models.CharField(max_length=128)
    created_at= models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'users'
    def __str__(self): return f"{self.full_name} ({self.role})"
