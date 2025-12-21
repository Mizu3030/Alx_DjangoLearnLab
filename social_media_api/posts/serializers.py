from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id", "post", "author", "author_username",
            "content", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "author", "author_username", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source="likes_count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "author", "author_username",
            "title", "content", "created_at", "updated_at",
            "comments", "likes_count"
        ]
        read_only_fields = ["id", "author", "author_username", "created_at", "updated_at", "comments", "likes_count"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "post", "user", "user_username", "created_at"]
        read_only_fields = ["id", "user", "user_username", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
