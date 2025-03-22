import secrets
from django.db import models

class APIToken(models.Model):
    """ Stores API tokens for authenticating external applications """
    token = models.CharField(max_length=64, unique=True, editable=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    description = models.CharField(max_length=255, blank=True, null=True)  

    def save(self, *args, **kwargs):
        """ Generate a secure token if none exists """
        if not self.token:
            self.token = secrets.token_hex(32)  # Secure 64-character token
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token: {self.token[:6]}... (Created {self.created_at})"