# views.py
from django.shortcuts import render
from Announcement.models import Announcement
from TrainingProgram.models import TrainingProgram
from Job_Opening.models import Job_Opening
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests



def landing_page(request):
    training_programs = TrainingProgram.objects.order_by('-id')[:5]
    announcements = Announcement.objects.order_by('-id')[:5]
    
    # Get the current date
    current_date = timezone.now()
    print(current_date)

    # Get only the job openings whose end of registration date is in the future
    job_openings = Job_Opening.objects.filter(end_of_registration__gte=current_date).order_by('-id')[:5]

    context = {
        'training_programs': training_programs,
        'announcements': announcements,
        'job_openings': job_openings,
    }

    return render(request, 'index.html', context)
