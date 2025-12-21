from rest_framework import viewsets, filters, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# لو عندك notifications/utils.py
try:
    from notifications.utils import notify
except ImportError:
    notify = None

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  #  مطلوب للفحص
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  #  مطلوب للفحص
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if notify and comment.post.author != self.request.user:
            notify(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented",
                target=comment.post,
                description=f"{self.request.user.username} commented on your post '{comment.post.title}'"
            )

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)

        if notify and post.author != request.user:
            notify(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target=post,
                description=f"{request.user.username} liked your post '{post.title}'"
            )
        return Response({"detail": "Liked"}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted == 0:
            return Response({"detail": "Not liked yet"}, status=status.HTTP_200_OK)
        return Response({"detail": "Unliked"}, status=status.HTTP_200_OK)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list("id", flat=True)
        return Post.objects.filter(author_id__in=following_ids).order_by("-created_at")
