# admin.py
from django.contrib import admin
from .models import TrainingProgram
from student.models import Student_Training_Registration
import pandas as pd
import io
import zipfile
from django.http import HttpResponse

def export_training_data(modeladmin, request, queryset):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for training in queryset:
            applicants = Student_Training_Registration.objects.filter(Training_ID=training)

            training_info = {
                'training_id': [training.id],
                'training_subject': [training.training_subject],
                'training_organization': [training.training_organization],
            }
            training_df = pd.DataFrame(training_info)

            student_details = {
                'S.No': list(range(1, len(applicants) + 1)),
                'Student ID': [app.Student_ID.Student_ID for app in applicants],
                'Username': [app.Student_ID.username for app in applicants],
                'Email': [app.Student_ID.email for app in applicants],
                'Branch': [app.Student_ID.Branch for app in applicants],
                #'Resume_Link': [app.Student_ID.Resume_Link for app in applicants],  # Update with the actual field name
                'CGPA': [app.Student_ID.CGPA for app in applicants],  # Update with the actual field name
            }
            student_df = pd.DataFrame(student_details)

            student_df['S.No'] = range(1, len(student_df) + 1)

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                training_df.to_excel(writer, index=False, sheet_name=f'Training_{training.id}', startrow=0)
                pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name=f'Training_{training.id}', startrow=training_df.shape[0] + 2)
                student_df.to_excel(writer, index=False, sheet_name=f'Training_{training.id}', startrow=training_df.shape[0] + 3)

            zip_file.writestr(f'Training_data_{training.id}.xlsx', excel_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=training_data.zip'

    return response

export_training_data.short_description = "Export Training' data"


class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('training_subject', 'prerequisites', 'training_organization', 'join_date', 'end_of_registration')
    actions = [export_training_data]
    search_fields = ('training_subject', 'training_organization',)

admin.site.register(TrainingProgram, TrainingProgramAdmin)
