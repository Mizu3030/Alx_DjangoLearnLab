from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class ActorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorMiniSerializer(read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'verb', 'actor', 'target_repr', 'created_at', 'read']

    def get_target_repr(self, obj):
        if obj.target is None:
            return None
        return str(obj.target)
