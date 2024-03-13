from django import forms
from django.utils import timezone

class TestForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class ChoiceForm(forms.Form):
    choice1 = forms.BooleanField(label="choice1")
    choice2 = forms.BooleanField(label="choice2")
    choice3 = forms.BooleanField(label="choice3")

class JobProfileForm(forms.Form):
    company = forms.CharField(label="Company", widget=forms.HiddenInput())
    def __init__(self, allJobs, *args, **kwargs):
        super(JobProfileForm, self).__init__(*args, **kwargs)
        for job in allJobs:
            status = job.end_of_registration < timezone.now().date()
            self.fields[job.id] = forms.BooleanField(label=job.JobProfile, required=False, disabled = status)