from django.contrib import admin

# Register your models here.
from .models import UserData, EmailValidation

admin.site.register(UserData)
admin.site.register(EmailValidation)
