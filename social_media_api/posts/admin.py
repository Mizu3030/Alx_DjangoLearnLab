# posts/admin.py
from django.contrib import admin
from .models import Post, Comment, Like

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "content", "created_at")
    readonly_fields = ("created_at",)

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    fields = ("user", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "updated_at", "likes_count")
    list_filter = ("author", "created_at")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "created_at"
    inlines = [CommentInline, LikeInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("content", "author__username", "post__title")
    date_hierarchy = "created_at"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "created_at")
    list_filter = ("created_at", "post__author")
    search_fields = ("post__title", "user__username")
    date_hierarchy = "created_at"
