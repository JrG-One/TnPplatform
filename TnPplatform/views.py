# views.py
from django.shortcuts import render
from Announcement.models import Announcement
from TrainingProgram.models import TrainingProgram
from Job_Opening.models import Job_Opening
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

from django.db.models import Max

from django.http import JsonResponse


def landing_page(request):
    training_programs = TrainingProgram.objects.order_by('-id')[:5]
    announcements = Announcement.objects.order_by('-id')[:5]
    
    # Get the current date
    current_date = timezone.now()
    print(current_date)

    # Get only the job openings whose end of registration date is in the future
    
    latest_job_openings = Job_Opening.objects.values('NameofCompany').annotate(max_id=Max('id'))

    # Get the unique instances based on the latest job openings
    job_openings = Job_Opening.objects.filter(id__in=latest_job_openings.values('max_id'))

    context = {
        'training_programs': training_programs,
        'announcements': announcements,
        'job_openings': job_openings,
    }

    return render(request, 'index.html', context)
    # return JsonResponse({'job_openings': job_openings})
