from rest_framework import serializers
from Timetracker.models import Employee, Project, WorkSession, Screenshot

class EmployeeSerializer(serializers.ModelSerializer):
    """ Serializes Employee data for the API """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    project = serializers.CharField(source="project.name", allow_null=True)

    class Meta:
        model = Employee
        fields = ["id", "username", "email", "job_title", "project"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "start_date"]

class WorkSessionSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name", allow_null=True)

    class Meta:
        model = WorkSession
        fields = ["id", "employee", "project", "clock_in", "clock_out", "duration"]

class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ["id", "work_session", "image_path", "timestamp"]
        read_only_fields = ["timestamp"]