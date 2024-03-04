# models.py
from django.db import models
# from student.models import Student

class TrainingProgram(models.Model):
    training_subject = models.CharField(max_length=200)
    prerequisites = models.TextField()
    training_organization = models.CharField(max_length=200)
    join_date = models.DateField()
    end_of_registration = models.DateField()

    # Students = models.ManyToManyField(Student, through = "Job_Student_Application")
    def __str__(self) -> str:
        return f"{self.training_subject}"