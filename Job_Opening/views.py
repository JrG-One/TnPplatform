from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect

from student.models import Job_Student_Application, Student
from .models import Job_Opening
from .serializer import JobOpeningSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import TestForm, ChoiceForm, JobProfileForm


class JobOpeningViewSet(viewsets.ModelViewSet):
    queryset = Job_Opening.objects.all()
    serializer_class = JobOpeningSerializer



@login_required(login_url="/accounts/google/login")
def job_opening_detail(request, NameofCompany):

    if Student.objects.get(username = request.user).Resume_Link =="blank":
        return redirect("/resume/")
    
    # print(Student.objects.get(username = request.user).Resume_Link)
    # print("request object -> ", request.GET, " ", pk)
    
    allJobs = Job_Opening.objects.filter(NameofCompany = NameofCompany)

    user_has_registered = Job_Student_Application.objects.filter(Student_ID=request.user, Job_ID=allJobs[0]).exists()

    print(user_has_registered)

    testForm = TestForm()
    company = allJobs[0].NameofCompany

    jobProfileForm = JobProfileForm(allJobs, initial= {"company": company})

    user_is_staff = Student.objects.get(email=request.user.email).is_staff

    context = {
        "testForm" : testForm,
        "JobProfileForm" : jobProfileForm,
        "Company" : company,
        "jobs" : allJobs ,
        "user_has_registered" : user_has_registered,
        "user_is_staff" : user_is_staff
    }

    return render(request, 'job_detail.html', context )


@login_required(login_url="/accounts/google/login")
def register_job(request):

    if request.method == "POST":
        postData = request.POST.copy()
        postData.pop('csrfmiddlewaretoken')
        company = postData.pop('company')

        id_list = list(postData.keys())
        print(id_list)

        for id in postData:
            job = Job_Opening.objects.get(id = id)
            if Job_Student_Application.objects.filter(Student_ID=request.user, Job_ID=job).exists() == False:
                Job_Student_Application.objects.create(Student_ID=request.user, Job_ID=job, Blocked=False, Status='A')
        return JsonResponse({'status': 'success'})
    # job = get_object_or_404(Job_Opening, pk=pk)

    # if job.end_of_registration < timezone.now().date():
    #     return HttpResponse('Registration for this job opening has closed.')

    return JsonResponse({'status': 'failure'})