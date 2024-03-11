from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobOpeningViewSet, job_opening_detail, register_job

router = DefaultRouter()
router.register(r'job_openings', JobOpeningViewSet, basename='job_opening')

urlpatterns = [
    path('job_openings/register', register_job, name='register_job'),
    path('job_openings/<str:NameofCompany>/', job_opening_detail, name='job_opening_detail'),
] + router.urls