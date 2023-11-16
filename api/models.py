from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tasks(models.Model):
    task = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    ismarked = models.BooleanField(default=False)
    def __str__(self):
        return self.task + ": state: " + str(self.ismarked)
