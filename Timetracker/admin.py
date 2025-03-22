from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from.views import send_activation_email
from .models import Employee, Project

# Create a Custom Form Without Password Fields
class CustomUserCreationForm(forms.ModelForm):
    """ Custom form for adding users in Django Admin without requiring passwords """

    email = forms.EmailField(required=True)  # Explicitly make email required

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # No password required
        if commit:
            user.save()
        return user

class EmployeeInline(admin.StackedInline):
    """ Allows adding Employee details (Job Title, Project) when creating a User """
    model = Employee
    extra = 1


class CustomUserAdmin(UserAdmin):
    """ Extends UserAdmin to include Employee creation """

    add_form = CustomUserCreationForm

    add_fieldsets = (
        ("User Info", {"fields": ("username", "email", "first_name", "last_name")}),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    inlines = [EmployeeInline]

    def save_model(self, request, obj, form, change):
        """ Ensure email is not empty, create Employee, and send activation email """
        if not obj.email:
            raise ValueError("Email cannot be empty!")

        is_new = not change

        if is_new:
            obj.is_active = False  # Set user as inactive before saving
            obj.set_unusable_password()  # Require them to set their own password

        super().save_model(request, obj, form, change)  # Save the user

        if is_new:
            send_activation_email(obj, request)  # Send activation email

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date")
    search_fields = ("name",)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "project")
    search_fields = ("user__username", "job_title")
    list_filter = ("project",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)