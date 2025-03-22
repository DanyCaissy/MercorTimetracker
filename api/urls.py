from django.urls import path
from .views import TestAuthentication

urlpatterns = [
    path("test_authentication/", TestAuthentication, name="Test_Authentication"),
]