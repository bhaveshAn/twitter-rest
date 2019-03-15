from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser
from user.models import Profile


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = ()
    search_fields = ("email", "username")
    ordering = ("email", "username")
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)  # Allow tweet to be editable on admin end
