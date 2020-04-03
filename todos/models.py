from django.db import models

# Create your models here.

class Todo(models.Model):
    """docstring for Todo."""
    content = models.TextField()
