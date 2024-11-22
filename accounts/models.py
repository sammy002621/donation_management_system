from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('standard', 'Standard User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='standard')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def is_admin_user(self):
        return self.user_type == 'admin'