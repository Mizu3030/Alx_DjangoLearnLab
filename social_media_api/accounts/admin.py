# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "bio", "profile_picture")}),
        ("Relationships", {"fields": ("followers",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    list_display = (
        "id", "username", "email", "first_name", "last_name",
        "followers_count", "following_count", "avatar_preview", "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions", "followers")

    def avatar_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="height:32px;width:32px;border-radius:50%;" />', obj.profile_picture.url)
        return "-"
    avatar_preview.short_description = "Avatar"
