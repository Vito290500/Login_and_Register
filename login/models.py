from django.db import models

class UserData(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class EmailValidation(models.Model):
    email = models.CharField(max_length=120, null=True)
    validation = models.BooleanField()
    otp = models.CharField(max_length=5, null=True)
    attempt = models.CharField(max_length=5, null=True, default=3)

    def __str__(self):
        return self.email