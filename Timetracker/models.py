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


class WorkSession(models.Model):
    """ Represents a work session (clock-in and clock-out) """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)  # Nullable until they clock out
    duration = models.PositiveIntegerField(null=True, blank=True)  # Stored in seconds (optional)

    def save(self, *args, **kwargs):
        """ Automatically calculate duration on save if clock_out is set """
        if self.clock_in and self.clock_out:
            self.duration = int((self.clock_out - self.clock_in).total_seconds())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.clock_in} to {self.clock_out or 'Active'}"

class Screenshot(models.Model):
    """ Stores screenshots taken during a work session """
    work_session = models.ForeignKey(WorkSession, on_delete=models.CASCADE, related_name="screenshots")
    timestamp = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=500)  # Path to the screenshot file

    def __str__(self):
        return f"Screenshot for {self.work_session.employee.user.username} at {self.timestamp}"