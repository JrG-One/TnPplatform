from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework import permissions

from .models import TrainingProgram
from .serializer import TrainingProgramSerializer
from student.models import Student_Training_Registration

class NoPermissions(BasePermission):
    def has_permission(self, request, view):
        return False

class CanAddTrainingProgram(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('TrainingProgram.add_training_program')

class CanChangeTrainingProgram(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('TrainingProgram.change_training_program')

class CanDeleteTrainingProgram(BasePermission):
    def has_permission(self, request, view):
        #print(f"User permissions: {request.user.get_all_permissions()}")
        return request.user.has_perm('TrainingProgram.delete_training_program')

class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny,]
        elif self.request.method == 'POST':
            self.permission_classes = [CanAddTrainingProgram,]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteTrainingProgram,]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [CanChangeTrainingProgram,]
        else:
            self.permission_classes = [NoPermissions,]
        return super(TrainingProgramViewSet, self).get_permissions()

def training_program_detail(request, pk):
    training_program = get_object_or_404(TrainingProgram, pk=pk)
    user_has_registered = Student_Training_Registration.objects.filter(Student_ID=request.user, Training_ID=training_program).exists()
    return render(request, 'training_program_detail.html', {'training_program': training_program, 'user_has_registered': user_has_registered})