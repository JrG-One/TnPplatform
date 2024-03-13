from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, announcement_detail, create_announcement

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement-list')

urlpatterns = [
    path('announcements/create', create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/', announcement_detail, name='announcement_detail'),
    path('', include(router.urls)),
]