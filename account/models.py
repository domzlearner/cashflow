
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # is_email_verified = models.BooleanField(default=False)
    # security_question = models.CharField(max_length=255, blank=True)
    # security_answer = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.email