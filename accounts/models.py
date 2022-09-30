from django.db import models
from django.contrib import admin
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.first_name

    @admin.display(ordering='user.first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user.last_name')
    def last_name(self):
        return self.user.last_name

    @admin.display(ordering='user.email')
    def email(self):
        return self.user.email