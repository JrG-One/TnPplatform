from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect

from student.models import Job_Student_Application, Student
from .models import Job_Opening
from .serializer import JobOpeningSerializer
from django.contrib.auth.decorators import login_required




class JobOpeningViewSet(viewsets.ModelViewSet):
    queryset = Job_Opening.objects.all()
    serializer_class = JobOpeningSerializer



@login_required(login_url="/accounts/google/login")
def job_opening_detail(request, pk):
    # print(Student.objects.get(username = request.user).Resume_Link)
    if Student.objects.get(username = request.user).Resume_Link =="blank":
        return redirect("/resume/")
    job = get_object_or_404(Job_Opening, pk=pk)
    user_has_registered = Job_Student_Application.objects.filter(Student_ID=request.user, Job_ID=job).exists()
    user_is_staff = Student.objects.get(email=request.user.email).is_staff
    return render(request, 'job_detail.html', {'job': job, 'user_has_registered': user_has_registered, "user_is_staff": user_is_staff})
