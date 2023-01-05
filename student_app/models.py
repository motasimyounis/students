from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.Title
    
    
class HomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)
    Description = models.TextField(max_length=500)
    Due = models.DateTimeField()
    Status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
    

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
         