from django.db import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthrosiedPersons(models.Model):
    user=models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

