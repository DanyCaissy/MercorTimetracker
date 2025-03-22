from django.contrib import admin
from .models import APIToken

@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ("token", "created_at", "description")
    readonly_fields = ("token", "created_at")
    search_fields = ("description",)

    def has_change_permission(self, request, obj=None):
        """ Prevent tokens from being modified after creation """
        return False