import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from Job_Opening.models import Job_Opening
from TrainingProgram.models import TrainingProgram
from .models import Job_Student_Application, Student_Training_Registration, Student
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json
from .utils import generate_pdf, store_pdf_in_drive
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("this is student page")

@login_required(login_url="/accounts/google/login")
def register_job(request, pk):
    job = get_object_or_404(Job_Opening, pk=pk)

    if job.end_of_registration < timezone.now().date():
        return HttpResponse('Registration for this job opening has closed.')
    
    Job_Student_Application.objects.create(Student_ID=request.user, Job_ID=job, Blocked=False, Status='A')
    return JsonResponse({'status': 'success'})

@login_required(login_url="/accounts/google/login")
def register_training(request,pk):
    trainingProgram = get_object_or_404(TrainingProgram, pk=pk)
    Student_Training_Registration.objects.create(Student_ID=request.user, Training_ID=trainingProgram, Attended=False)
    return JsonResponse({'status': 'success'})

@login_required(login_url="/accounts/google/login")
def resume(request):
    json1 = Student.objects.get(username=request.user).resume_json 
    if json1=='blank':
        json1 = {}

    if request.method =="POST":
        jsonData = json.loads(request.body.decode('utf-8')) 
        student_id = Student.objects.get(username=request.user).Student_ID
        json_file = jsonData['json'][0]
        student_instance, created = Student.objects.get_or_create(Student_ID=student_id)
        # Update the json field and save the instance
        student_instance.resume_json= json_file
        # student_instance.save()


        # pdf_file = f"temp/Resume-{student_id}-{datetime.datetime.now()}.pdf"  
        pdf_data = generate_pdf(json_file)
        print("=========================================")
        # Call the function to store PDF in Google Drive
        x = store_pdf_in_drive(request.user, pdf_data, file_name='Resume.pdf')
        # st = Student.objects.get(Student_ID=student_id)
        student_instance.Resume_Link = "https://drive.google.com/file/d/"+x 
        # student_instance.resume_json = json_file
        student_instance.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(json)
    return render(request, "Resume_generator.html", {"user": json1})

# from django.views import View
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator
# from django.shortcuts import get_object_or_404
# from .models import Student, Job_Student_Application, Job_Opening
# import io
# import os

# @method_decorator(staff_member_required, name='dispatch')
# class ExcelGeneratorAdminView(View):
#     def get(self, request):
#         students = Student.objects.all()

#         data = {
#             'Student ID': [student.Student_ID for student in students],
#             'Name': [f"{student.first_name} {student.last_name}" for student in students],
#             'Branch': [student.Branch for student in students],
#             'CGPA': [student.CGPA for student in students],
#         }

#         df = pd.DataFrame(data)

#         excel_buffer = io.BytesIO()
#         df.to_excel(excel_buffer, index=False, sheet_name='Students')
#         excel_buffer.seek(0)

#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=student_data.xlsx'
#         response.write(excel_buffer.read())

#         return response

# def export_student_data(request, student_id):
#     student = get_object_or_404(Student, Student_ID=student_id)
#     applications = Job_Student_Application.objects.filter(Student_ID=student)

#     student_info = {
#         'Student ID': [student.Student_ID],
#         'Username': [student.username],
#         'Email': [student.email],
#         'Branch': [student.Branch],
#     }
#     student_df = pd.DataFrame(student_info)

#     job_details = {
#         'Job ID': [app.Job_ID.id if app.Job_ID else "N/A" for app in applications],
#         'Company': [app.Job_ID.NameofCompany if app.Job_ID else "N/A" for app in applications],
#         'Position': [app.Job_ID.JobProfile if app.Job_ID else "N/A" for app in applications],
#     }
#     job_df = pd.DataFrame(job_details)
    
#     job_df['S.No'] = range(1, len(job_df) + 1)
#     with pd.ExcelWriter('student_data.xlsx', engine='xlsxwriter') as writer:
#         student_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=0)
#         pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name='Sheet1', startrow=student_df.shape[0] + 2)
#         job_df[['S.No', 'Job ID', 'Company', 'Position']].to_excel(writer, index=False, sheet_name='Sheet1', startrow=student_df.shape[0] + 3)

#     file_path = 'student_data.xlsx'

#     with open(file_path, 'rb') as excel_file:
#         response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = f'attachment; filename=student_data_{student_id}.xlsx'

#     os.remove(file_path)

#     return response


# def export_job_data(request, job_id):
#     job = get_object_or_404(Job_Opening, id=job_id)
#     applicants = Job_Student_Application.objects.filter(Job_ID=job)

#     job_info = {
#         'Job ID': [job.id],
#         'Company': [job.NameofCompany],
#         'Profile': [job.JobProfile],
#         'CTC': [job.ctc],
#     }
#     job_df = pd.DataFrame(job_info)

#     student_details = {
#         'S.No': list(range(1, len(applicants) + 1)), 
#         'Student ID': [app.Student_ID.Student_ID for app in applicants],
#         'Username': [app.Student_ID.username for app in applicants],
#         'Email': [app.Student_ID.email for app in applicants],
#         'Branch': [app.Student_ID.Branch for app in applicants],
#     }
#     student_df = pd.DataFrame(student_details)

#     student_df['S.No'] = range(1, len(student_df) + 1)

#     with pd.ExcelWriter('job_data.xlsx', engine='xlsxwriter') as writer:
#         job_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=0)
#         pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name='Sheet1', startrow=job_df.shape[0] + 2)
#         pd.DataFrame([['Student Applications']]).to_excel(writer, index=False, sheet_name='Sheet1', startrow=job_df.shape[0] + 3)
#         student_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=job_df.shape[0] + 4)

#     file_path = 'job_data.xlsx'

#     with open('job_data.xlsx', 'rb') as excel_file:
#         response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = f'attachment; filename=job_data_{job_id}.xlsx'
    
#     os.remove(file_path)

#     return response
