# from django.contrib import admin
# from Job_Opening.models import Job_Opening

# class JobAdmin(admin.ModelAdmin):
#     #list_display = ('NameofCompany', 'profileOfCompany', 'JobProfile', 'BranchChoice', 'ctc', 'Eligibility', 'Selection', 'location', 'stipend', 'join_date','end_of_registration')

#    list_display = ('Name_of_Company', 'Profile_Of_Company', 'Job_Profile', 'Branch_Choice', 'CTC', 'Eligibility_Criteria', 'Selection', 'Location', 'Stipend_per_month','join_date','end_of_registration')

# admin.site.register(Job_Opening,JobAdmin)

from django.contrib import admin
from .models import Job_Opening
from student.models import Job_Student_Application
import pandas as pd
import io
import zipfile
from django.http import HttpResponse

def export_job_data(modeladmin, request, queryset):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for job in queryset:
            applicants = Job_Student_Application.objects.filter(Job_ID=job)

            job_info = {
                'Job ID': [job.id],
                'Company': [job.NameofCompany],
                'Profile': [job.JobProfile],
                'CTC': [job.ctc],
            }
            job_df = pd.DataFrame(job_info)

            student_details = {
                'S.No': list(range(1, len(applicants) + 1)),
                'Student ID': [app.Student_ID.Student_ID for app in applicants],
                'Username': [app.Student_ID.username for app in applicants],
                'Email': [app.Student_ID.email for app in applicants],
                'Branch': [app.Student_ID.Branch for app in applicants],
                'Resume_Link' : [app.Student_ID.Resume_Link for app in applicants],
                'CGPA' : [app.Student_ID.CGPA for app in applicants]
            }
            student_df = pd.DataFrame(student_details)

            student_df['S.No'] = range(1, len(student_df) + 1)

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                job_df.to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=0)
                pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=job_df.shape[0] + 2)
                student_df.to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=job_df.shape[0] + 3)

            zip_file.writestr(f'job_data_{job.id}.xlsx', excel_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=jobs_data.zip'

    return response

export_job_data.short_description = "Export selected jobs' data"

class JobAdmin(admin.ModelAdmin):
    list_display = ('id','NameofCompany', 'profileOfCompany', 'JobProfile', 'BranchChoice', 'ctc', 'Eligibility', 'Selection', 'location', 'stipend', 'join_date', 'end_of_registration')
    actions = [export_job_data]
    search_fields = ("id","NameofCompany",)

admin.site.register(Job_Opening, JobAdmin)
