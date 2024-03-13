from django.forms import ModelForm
from .models import Announcement

class announcementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content","attachmentLink","attachmentFile"]

