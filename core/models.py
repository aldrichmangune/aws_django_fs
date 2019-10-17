from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class S3File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
    description = models.CharField(max_length=50)