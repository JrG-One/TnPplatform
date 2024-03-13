from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Announcement
from .serializer import AnnouncementSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import announcementForm
from django.http import JsonResponse

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    
@api_view(['GET'])
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcement_detail.html', {'announcement': announcement})

def create_announcement(request):

    if request.method == "POST":
        form = announcementForm(request.POST, request.FILES) # FILES contains file uploaded
        if form.is_valid():
            # here the data from form can be processed. it will be in the variable named "cleaned_data".
            print(form.cleaned_data)

            # method that save data to database.
            form.save()
            return JsonResponse({"status":"success", "formdata":form.cleaned_data})
    
    # if GET the send an empty instance of form to the frontend.
    form = announcementForm()
    return render(request, "announcement_form.html", {"form": form})