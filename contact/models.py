from django.db import models

# Create your models here.

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length = 62)
    message = models.TextField(max_length = 510)