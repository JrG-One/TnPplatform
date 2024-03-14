from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingProgramViewSet, training_program_detail

router = DefaultRouter()
router.register(r'training_programs', TrainingProgramViewSet, basename='training_program')

urlpatterns = [
    path('training_programs/<int:pk>/', training_program_detail, name='training_program_detail')
]+router.urls