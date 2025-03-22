from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    """ Represents a project in the system """
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    """ Represents an employee, linked to a Django User """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"