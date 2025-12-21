from django.urls import path
from .views import NotificationListView, MarkAllReadView, MarkReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('mark-all-read/', MarkAllReadView.as_view(), name='notifications-mark-all-read'),
    path('<int:pk>/mark-read/', MarkReadView.as_view(), name='notifications-mark-read'),
]
