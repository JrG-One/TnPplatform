# TnPplatform/urls.py
from django.contrib import admin
from django.urls import path, include
# from student.admin import custom_admin_site
from . import views

'''
making initialization and testing easier 


Edit(Vedic):-Keep following snippet commented during migrate --run-syncdb 
'''
from django.contrib.sites.models import Site
from student.models import Student
from allauth.socialaccount.models import SocialApp
import os

import sys

if 'runserver' in sys.argv:
    if not Student.objects.filter(username=os.getenv("username")).exists():
        Student.objects.create_superuser(username=os.getenv("username"),email=os.getenv("email"), password=os.getenv("password"))
    if not Site.objects.filter(domain="127.0.0.1:8000").exists():
        Site.objects.create(name="127.0.0.1:8000", domain="127.0.0.1:8000")
    if not SocialApp.objects.filter(provider="google").exists():
        SocialApp.objects.create(provider="google", name="Google", client_id=os.getenv("client"), secret=os.getenv("secret")).sites.set(Site.objects.filter(domain="127.0.0.1:8000"))





urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('', views.landing_page, name='landing_page'),
    # path('resume/', views.index, name='index'),
    path('', include('Announcement.urls')),
    path('', include('Job_Opening.urls')),
    path('', include('TrainingProgram.urls')),
    path('', include('student.urls')),
    path('admin/', include('student.urls')),
    # path('admin/student/', custom_admin_site.urls),
    path('student/', include('student.urls')),

]
