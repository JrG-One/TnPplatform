from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Announcement
from .serializer import AnnouncementSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class NoPermissions(BasePermission):
    def has_permission(self, request, view):
        return False

class CanAddAnnouncement(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('Announcement.add_announcement')

class CanDeleteAnnouncement(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('Announcement.delete_announcement')

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny,]
        elif self.request.method == 'POST':
            self.permission_classes = [CanAddAnnouncement,]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteAnnouncement,]
        else:
            self.permission_classes = [NoPermissions,]
        return super(AnnouncementViewSet, self).get_permissions()

@api_view(['GET'])
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcement_detail.html', {'announcement': announcement})