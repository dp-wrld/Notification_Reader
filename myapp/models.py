import email
from django.db import models


class Notification(models.Model):
    androidid = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    msg = models.CharField(max_length=512, blank=True, null=True)
    # image = models.ImageField(upload_to='uploads')
    package = models.CharField(max_length=10, blank=True, null=True)
    RegDate = models.DateField(blank=True, null=True)
    ntime = models.TimeField(blank=True, null=True)
    reciveDate = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.androidid


class Login(models.Model):
    user = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self) -> str:
        return self.user


class Device(models.Model):
    dname = models.CharField(max_length=30, blank=True, null=True)
    androidid = models.CharField(
        max_length=40, blank=True, null=True, unique=True)
    androidid1 = models.CharField(
        max_length=40, blank=True, null=True, unique=True)
    androidid2 = models.CharField(
        max_length=40, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return self.dname


class RegistrationDetais(models.Model):
    androidid = models.CharField(max_length=40, blank=True, null=True)
    androidid1 = models.CharField(max_length=40, blank=True, null=True)
    androidid2 = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField()
    ntime = models.TimeField(blank=True, null=True)
    ncount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.username
