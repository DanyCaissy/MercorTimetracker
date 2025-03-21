from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import UserProfile
from .views import send_activation_email

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

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm  # Replace Django's default form

    add_fieldsets = (
        ("User Info", {"fields": ("username", "email", "first_name", "last_name")}),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    def save_model(self, request, obj, form, change):
        """ Ensure email is not empty and set user inactive by default """
        if not obj.email:
            raise ValueError("Email cannot be empty!")  # Prevent saving without email

        if not change:  # If the user is being created, not updated
            obj.is_active = False  # Default inactive
            obj.set_unusable_password()  # Prevents login until user sets their own password
            obj.save()
            send_activation_email(obj, request)  # Send activation email

        super().save_model(request, obj, form, change)  # Call the original save method

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)