# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "recipient", "actor", "verb", "target_object_id",
        "created_at", "read",
    )
    list_filter = ("verb", "read", "created_at")
    search_fields = ("recipient__username", "actor__username", "verb", "description")
    date_hierarchy = "created_at"
    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f"Marked {updated} notifications as read.")
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(read=False)
        self.message_user(request, f"Marked {updated} notifications as unread.")
    mark_as_unread.short_description = "Mark selected as unread"
