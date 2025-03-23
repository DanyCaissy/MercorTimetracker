from django.urls import path
from .views import (
    list_create_projects, project_detail,
    clock_in, clock_out, get_work_sessions,
    upload_screenshot, get_screenshots, list_employees,
    get_employee, login_api
)

urlpatterns = [
    path("employees/", list_employees, name="employee-list"),
    path("employees/<int:employee_id>/", get_employee, name="employee-detail"),

    path("projects/", list_create_projects, name="project-list"),
    path("projects/<int:project_id>/", project_detail, name="project-detail"),

    # WorkSessions
    path("worksession/clock-in/", clock_in, name="worksession-clockin"),
    path("worksession/clock-out/", clock_out, name="worksession-clockout"),
    path("worksession/<int:employee_id>/", get_work_sessions, name="worksession-list"),

    # Screenshots
    path("screenshots/upload/", upload_screenshot, name="screenshot-upload"),
    path("screenshots/<int:session_id>/", get_screenshots, name="screenshot-list"),

    path("login/", login_api, name="login_api"),
]