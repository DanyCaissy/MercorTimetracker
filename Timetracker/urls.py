from django.urls import path

from . import views
from .views import activate, dashboard

urlpatterns = [
    path("", views.index, name="index"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("dashboard/", dashboard, name="dashboard"),
]