from email.policy import default
from random import choice
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Group(models.Model):
    name = models.CharField(max_length=120)
    num_active = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    seenCounts = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title