from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from TrainingProgram.models import TrainingProgram
from Job_Opening.models import Job_Opening
from allauth.socialaccount.models import SocialAccount
from django.conf import settings


from .managers import StudentManager

# Create your models here.
class Student(AbstractUser):
    """
    first name, last name, email and other permission related things are inherited from abstractUser class.

    removed username field and made email field required.

    using custom manager StudentManager

    Student_ID is self Generating from the given email 
    """

    # email = models.EmailField(("email address"), unique=True)
    # REQUIRED_FIELDS = []

    # Additional Fields
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    personal_email = models.EmailField(("personal email address"), blank=True)
    # enrollment_no = models.CharField(max_length=20, unique=True, blank=True)
    # phone_number = models.CharField(max_length=15, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    # Existing Fields
    Student_ID = models.CharField(max_length=20, default="studentID", unique=True)
    BRANCH_CHOICES = [
        ("CSE", "CSE"),
        ("ECE", "ECE"),
    ]
    Branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    Resume_Link = models.CharField(max_length=300, default="blank")
    CGPA = models.DecimalField(max_digits=3, decimal_places=2, default="5.00")
    Block_All_Applications = models.BooleanField(default=False)
    Placed = models.ForeignKey(Job_Opening, null=True, blank=True, on_delete=models.CASCADE)
    Access_Token = models.CharField(max_length=300, null=True)
    resume_json = models.JSONField(null=True, blank=True)

    # using personal model manager
    # objects = StudentManager();

    def __str__(self):
        # if self.first_name:
        #     return f"{self.first_name} {self.last_name}"
        # else:
        return self.username
    
    # method that extracts roll no from email
    def save(self, *args, **kwargs):
        self.Student_ID = self.email.split('@')[0]
        self.Branch = self.email[4:6].upper()+"E" #CS/EC+E
        super(Student, self).save(*args, **kwargs)

class Student_Training_Registration(models.Model):
    Student_ID = models.ForeignKey(Student, on_delete = models.CASCADE)
    Training_ID = models.ForeignKey(TrainingProgram, on_delete = models.CASCADE)
    Attended = models.BooleanField()

class Job_Student_Application(models.Model):
    Student_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    Job_ID = models.ForeignKey('Job_Opening.Job_Opening', on_delete=models.CASCADE)  # Use the string format to avoid circular import
    Blocked = models.BooleanField()
    Status = models.CharField(max_length=1)


@receiver(post_save, sender = SocialAccount)
def create_profile(sender, instance, created, **kwargs):
    if created:
       # Grabbing data from social account to create profile for that user
       profile, created=Student.objects.get_or_create(username=instance.user)
    #    profile.Student_ID = instance.user
    #    profile.save()
