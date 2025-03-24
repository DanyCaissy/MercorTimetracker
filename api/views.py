
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Timetracker.models import Project, WorkSession, Screenshot, Employee
from .serializers import ProjectSerializer, WorkSessionSerializer, ScreenshotSerializer, EmployeeSerializer
from django.contrib.auth import authenticate


@api_view(["POST"])
def login_api(request):
    """Authenticate user and return user_id + employee_id (if exists)"""
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        # Get employee_id if the user is an employee
        employee = Employee.objects.filter(user=user).first()
        employee_id = employee.id if employee else None

        return JsonResponse({
            "status": "success",
            "user_id": user.id,
            "employee_id": employee_id
        }, status=200)

    return JsonResponse({"status": "failed", "error": "Invalid credentials"}, status=401)

@api_view(["GET"])
def list_employees(request):
    """ List all employees (Middleware already checks authentication) """
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(["GET"])
def get_employee(request, employee_id):
    """ Get a single employee by ID (Middleware already checks authentication) """
    try:
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeSerializer(employee)
        return JsonResponse(serializer.data, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


@api_view(["GET", "POST"])
def list_create_projects(request):
    """ List all projects or create a new one """
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def project_detail(request, project_id):
    """ Retrieve, update, or delete a project """
    try:
        project = Project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def clock_in(request):
    """ Clock-in an employee to a work session """
    employee_id = request.data.get("employee_id")
    mac_address = request.data.get("mac_address")

    try:
        employee = Employee.objects.get(id=employee_id)

        # Prevent duplicate clock-ins
        if WorkSession.objects.filter(employee=employee, clock_out__isnull=True).exists():
            return Response({"error": "Employee is already checked in"}, status=status.HTTP_400_BAD_REQUEST)

        project = employee.project if employee.project else None

        ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip_address:
            ip_address = ip_address.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        session = WorkSession.objects.create(
            employee=employee,
            project=project,
            clock_in=now(),
            ip_address=ip_address,
            mac_address=mac_address
        )

        serializer = WorkSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ObjectDoesNotExist:
        return Response({"error": "Invalid employee"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def clock_out(request):
    """ Clock-out an employee from a work session """
    employee_id = request.data.get("employee_id")

    try:
        session = WorkSession.objects.filter(employee__id=employee_id, clock_out__isnull=True).first()
        if not session:
            return Response({"error": "No active session found"}, status=status.HTTP_400_BAD_REQUEST)

        session.clock_out = now()
        session.save()
        serializer = WorkSessionSerializer(session)
        return Response(serializer.data)

    except ObjectDoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_work_sessions(request, employee_id):
    """ Get all work sessions for an employee, or return the most recent X sessions if 'limit' is provided """
    try:
        employee = Employee.objects.get(id=employee_id)
    except ObjectDoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the 'limit' parameter from the request (optional)
    limit = request.query_params.get("limit")

    # Fetch work sessions, ordered by most recent first
    sessions = WorkSession.objects.filter(employee=employee).order_by("-clock_in")

    # Apply limit if specified and valid
    if limit and limit.isdigit():
        sessions = sessions[:int(limit)]

    serializer = WorkSessionSerializer(sessions, many=True)
    return Response(serializer.data)


### --- Screenshot Endpoints ---
@api_view(["POST"])
def upload_screenshot(request):
    """ Upload a screenshot for a valid work session """

    work_session_id = request.data.get("work_session")

    try:
        work_session = WorkSession.objects.get(id=work_session_id)
    except ObjectDoesNotExist:
        return Response({"error": "Invalid work session ID"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure an image file is uploaded
    if "image_path" not in request.FILES:
        return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES["image_path"]
    file_path = f"media/screenshots/{uploaded_file.name}"  # Save in media/screenshots/

    # Save file to media folder
    with open(file_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # Save the screenshot record
    screenshot = Screenshot.objects.create(work_session=work_session, image_path=file_path)

    return Response({"message": "Screenshot uploaded successfully!", "file_path": file_path},
                    status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_screenshots(request, session_id):
    """ Get all screenshots for a specific work session """
    screenshots = Screenshot.objects.filter(work_session__id=session_id)
    serializer = ScreenshotSerializer(screenshots, many=True)
    return Response(serializer.data)