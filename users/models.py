from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    USER_CHOICES = (
        ('regular', 'REGULAR'),
        ('premium', 'PREMIUM')
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=40, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    about = models.TextField(blank=True)
    role = models.CharField(max_length=15, choices=USER_CHOICES, default='regular')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    genres = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)