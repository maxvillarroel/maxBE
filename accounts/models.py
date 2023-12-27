from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class AccountRequest(models.Model):
    username = models.CharField(max_length=150, help_text= "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", validators=[UnicodeUsernameValidator()])
    email = models.EmailField()
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)