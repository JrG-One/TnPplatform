from django.db import models
# from student.models import Student

class Job_Opening(models.Model):
    NameofCompany = models.CharField(max_length=200)
    profileOfCompany = models.TextField()

    JobProfile = models.CharField(max_length=100)
    JobDescription = models.TextField()
    EmploymentType = models.CharField(max_length=100)
    

    Website = models.CharField(max_length = 200, null=True)
    Linkedin = models.CharField(max_length = 200, null = True)

    Address = models.CharField(max_length=100)
    Worklocation = models.CharField(max_length=100)

    # Use choices for fields with predefined options
    BRANCH_CHOICES = [
        ("CSE", "Computer Science and Engineering"),
        ("ECE", "Electronics and Engineering"),
        ("both", "both")
    ]
    BranchChoice = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    Eligibility = models.TextField()
    
    stipend = models.CharField(max_length = 200)
    ctc = models.CharField(max_length = 200)
    
    # SELECTION_CHOICES = [
    #     ("Virtual", "Virtual"),
    #     ("Offline", "Offline"),
    # ]
    # Selection = models.CharField(max_length=10, choices=SELECTION_CHOICES)
    
    Bond = models.CharField(max_length = 100 ,null = True)

    SelectionProcess = models.TextField()

    start = models.DateField()
    join_date = models.DateField()
    end_of_registration = models.DateField()

    def __str__(self):
        return f"{self.NameofCompany}"
