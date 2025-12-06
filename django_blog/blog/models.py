from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    def get_update_url(self):
        return reverse("comment_update", kwargs={"post_pk": self.post.pk, "pk": self.pk})

    def get_delete_url(self):
        return reverse("comment_delete", kwargs={"post_pk": self.post.pk, "pk": self.pk})
