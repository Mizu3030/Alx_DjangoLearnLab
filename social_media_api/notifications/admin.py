from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'target', 'created_at', 'read')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    list_filter = ('verb', 'read', 'created_at')
    ordering = ('-created_at',)
