from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username")
    recipient_username = serializers.ReadOnlyField(source="recipient.username")
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id", "recipient", "recipient_username",
            "actor", "actor_username",
            "verb", "description",
            "target_object_id", "target_type",
            "created_at", "read",
        ]
        read_only_fields = [
            "id", "recipient", "recipient_username",
            "actor", "actor_username",
            "created_at", "target_object_id", "target_type"
        ]

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
