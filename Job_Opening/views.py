from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.permissions import BasePermission

from student.models import Job_Student_Application, Student
from .models import Job_Opening
from .serializer import JobOpeningSerializer
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import permissions

class NoPermissions(BasePermission):
    def has_permission(self, request, view):
        return False

class CanAddJobOpening(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('Job_Opening.add_job_opening')

class CanChangeJobOpening(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('Job_Opening.change_job_opening')

class CanDeleteJobOpening(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('Job_Opening.delete_job_opening')

class JobOpeningViewSet(viewsets.ModelViewSet):
    queryset = Job_Opening.objects.all()
    serializer_class = JobOpeningSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny,]
        elif self.request.method == 'POST':
            self.permission_classes = [CanAddJobOpening,]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteJobOpening,]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [CanChangeJobOpening,]
        else:
            self.permission_classes = [NoPermissions,]
        return super(JobOpeningViewSet, self).get_permissions()

@login_required(login_url="/accounts/google/login")
def job_opening_detail(request, pk):
    if Student.objects.get(username = request.user).Resume_Link =="blank":
        return redirect("/student/resume/")
    job = get_object_or_404(Job_Opening, pk=pk)
    user_has_registered = Job_Student_Application.objects.filter(Student_ID=request.user, Job_ID=job).exists()
    user_is_staff = Student.objects.get(email=request.user.email).is_staff
    return render(request, 'job_detail.html', {'job': job, 'user_has_registered': user_has_registered, "user_is_staff": user_is_staff})