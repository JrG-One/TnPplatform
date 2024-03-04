from typing import Any
from django.contrib import admin
from django.urls import path
import pandas as pd
# from .views import export_student_data
from .models import Student, Job_Student_Application, Job_Opening, Student_Training_Registration, TrainingProgram
import io
import os
import zipfile
from django.http import HttpResponse
from Job_Opening.admin import JobAdmin
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

class YearFilter(admin.SimpleListFilter):

    # heading of the filter
    title = "year"

    # name passed in url of query
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """
        this is the list where the values on the right side are the filter option's names.
        """
        return [
            (('UI20'),('4th Year')),
            (('UI21'),('3rd Year')),
            (('UI22'),('2nd Year')),
            (('UI23'),('1st Year')),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset
        
        # returns entries for 4th year
        if self.value() == 'UI20':
            return queryset.filter(Student_ID__startswith = 'UI20')
        
        # returns entries for 3rd year
        if self.value() == 'UI21':
            return queryset.filter(Student_ID__startswith = 'UI21')
        
        # returns entries for 2nd year
        if self.value() == 'UI22':
            return queryset.filter(Student_ID__startswith = 'UI22')
        
        # returns entries for 1st year
        if self.value() == 'UI23':
            return queryset.filter(Student_ID__startswith = 'UI23')
    
class PlacedFilter(admin.SimpleListFilter):

    # heading of the filter
    title = "Placements"

    # name passed in url of query
    parameter_name = "placed"


    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset

        # returns entries for 4th year
        if self.value() == 'UI20':
            return queryset.filter(Student_ID__startswith = 'UI20')

        # returns entries for 3rd year
        if self.value() == 'UI21':
            return queryset.filter(Student_ID__startswith = 'UI21')

        # returns entries for 2nd year
        if self.value() == 'UI22':
            return queryset.filter(Student_ID__startswith = 'UI22')

        # returns entries for 1st year
        if self.value() == 'UI23':
            return queryset.filter(Student_ID__startswith = 'UI23')

class PlacedFilter(admin.SimpleListFilter):

    # heading of the filter
    title = "Placements"

    # name passed in url of query
    parameter_name = "placed"

    def lookups(self, request, model_admin):
        """
        this is the list where the values on the right side are the filter option's names.
        """
        return [
            (('not_placed'),('Not placed')),
            (('placed'),('Placed')),
        ]

    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset

        if self.value() == 'placed':
            return queryset.exclude(Placed = None) 

        if self.value() == 'not_placed':
            return queryset.filter(Placed = None) 

class PackageCategoryFilter(admin.SimpleListFilter):

    # heading of the filter
    title = "Package Category"

    # name passed in url of query
    parameter_name = "category"

    def lookups(self, request, model_admin):
        """
        this is the list where the values on the right side are the filter option's names.
        """
        return [
            (('A'),('A')),
            (('B'),('B')),
        ]

    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset

        if self.value() == 'A':
            return queryset.filter(CGPA__gte = 7.5) 

        if self.value() == 'B':
            return queryset.filter(CGPA__lt = 7.5)

def export_student_data(modeladmin, request, queryset):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for student in queryset:
            applications = Job_Student_Application.objects.filter(Student_ID=student)

            student_info = {
                'Student ID': [student.Student_ID],
                'Username': [student.username],
                'Email': [student.email],
                'Branch': [student.Branch],
            }
            student_df = pd.DataFrame(student_info)

            job_details = {
                'S.No': range(1, len(student.job_student_application_set.all()) + 1),
                'Job ID': [app.Job_ID.id if app.Job_ID else "N/A" for app in applications],
                'Company': [app.Job_ID.NameofCompany if app.Job_ID else "N/A" for app in applications],
                'Position': [app.Job_ID.JobProfile if app.Job_ID else "N/A" for app in applications],
            }
            job_df = pd.DataFrame(job_details)

            job_df['S.No'] = range(1, len(job_df) + 1)

            training_program_details = {
                'S.No': range(1, len(student.student_training_registration_set.all()) + 1),
                'Training ID': [registration.Training_ID.id if registration.Training_ID else "N/A" for registration in student.student_training_registration_set.all()],
                'Program Name': [registration.Training_ID.training_subject if registration.Training_ID else "N/A" for registration in student.student_training_registration_set.all()],
                'Attended': [registration.Attended for registration in student.student_training_registration_set.all()],
            }
            training_program_df = pd.DataFrame(training_program_details)

            # training_program_df['S.No'] = range(1, len(training_program_df) + 1)

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                student_df.to_excel(writer, index=False, sheet_name='Job_Applications', startrow=0)
                pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name='Job_Applications', startrow=student_df.shape[0] + 2)
                job_df.to_excel(writer, index=False, sheet_name='Job_Applications', startrow=student_df.shape[0] + 3)

                # Add an empty row between sheets
                pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name='Job_Applications', startrow=student_df.shape[0] + job_df.shape[0] + 5)

                student_df.to_excel(writer, index=False, sheet_name='Training_Programs', startrow=0)
                training_program_df.to_excel(writer, index=False, sheet_name='Training_Programs', startrow=student_df.shape[0] + job_df.shape[0] + 6)

            zip_file.writestr(f'student_data_{student.Student_ID}.xlsx', excel_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=students_data.zip'

    return response

export_student_data.short_description = "Export selected students' data"


# def export_job_data(modeladmin, request, queryset):
#     zip_buffer = io.BytesIO()

#     with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
#         for job in queryset:
#             applicants = Job_Student_Application.objects.filter(Job_ID=job)

#             job_info = {
#                 'Job ID': [job.id],
#                 'Company': [job.NameofCompany],
#                 'Profile': [job.JobProfile],
#                 'CTC': [job.ctc],
#             }
#             job_df = pd.DataFrame(job_info)

#             student_details = {
#                 'S.No': list(range(1, len(applicants) + 1)),
#                 'Student ID': [app.Student_ID.Student_ID for app in applicants],
#                 'Username': [app.Student_ID.username for app in applicants],
#                 'Email': [app.Student_ID.email for app in applicants],
#                 'Branch': [app.Student_ID.Branch for app in applicants],
#             }
#             student_df = pd.DataFrame(student_details)

#             student_df['S.No'] = range(1, len(student_df) + 1)

#             excel_buffer = io.BytesIO()
#             with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
#                 job_df.to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=0)
#                 pd.DataFrame([[]]).to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=job_df.shape[0] + 2)
#                 student_df.to_excel(writer, index=False, sheet_name=f'Job_{job.id}', startrow=job_df.shape[0] + 3)

#             zip_file.writestr(f'job_data_{job.id}.xlsx', excel_buffer.getvalue())

#     zip_buffer.seek(0)
#     response = HttpResponse(zip_buffer.read(), content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename=jobs_data.zip'

#     return response

# export_job_data.short_description = "Export selected jobs' data"

class StudentAdmin(admin.ModelAdmin):
    actions = [export_student_data]
    list_display = ('Student_ID', 'username', 'email', 'Branch', 'CGPA')
    list_filter = ("Branch",YearFilter, PlacedFilter, PackageCategoryFilter)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Student info', {'fields': ('Student_ID', 'Branch', 'Resume_Link', 'CGPA', 'Block_All_Applications','Placed')}),)
    search_fields = ("username","email", "Branch", "Student_ID")
#class JobAdmin(admin.ModelAdmin):
#     actions = [export_job_data]
#     list_display = ('id', 'NameofCompany', 'JobProfile', 'ctc')

class PackageCategoryFilter(admin.SimpleListFilter):
    
    # heading of the filter
    title = "Package Category"

    # name passed in url of query
    parameter_name = "category"

    def lookups(self, request, model_admin):
        """
        this is the list where the values on the right side are the filter option's names.
        """
        return [
            (('A'),('A')),
            (('B'),('B')),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset
        
        if self.value() == 'A':
            return queryset.filter(CGPA__gte = 7.5) 
        
        if self.value() == 'B':
            return queryset.filter(CGPA__lt = 7.5)

# Register your models here.
# class StudentAdmin(UserAdmin, ImportExportModelAdmin, ExportActionModelAdmin):

#     resource_classes = [StudentResource]

#     list_filter = ("Branch",YearFilter, PlacedFilter, PackageCategoryFilter)

#     list_display = ('username','email','first_name','last_name','Student_ID', 'Branch', 'Resume_Link', 'CGPA', 'Block_All_Applications','Placed', 'Access_Token','resume_json')


#     # list_editable = ('Student_ID',)

#     ordering = ("email",)

#     fieldsets = (
#         (None, {'fields': ('username','email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Student info', {'fields': ('Student_ID', 'Branch', 'Resume_Link', 'CGPA', 'Block_All_Applications','Placed')}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": (
#                 "email", "password1", "password2", "is_staff",
#                 "is_active", "groups", "user_permissions"
#             )}
#         ),
#     )
#     search_fields = ("username","email", "Branch", "Student_ID", )

class TrainingRegAdmin(admin.ModelAdmin):
    list_display = ('Student_ID','Training_ID','Attended')
    search_fields = ('Student_ID__Student_ID', 'Training_ID__training_subject')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('Student_ID','Job_ID','Blocked', 'Status')
    search_fields = ('Student_ID__Student_ID', 'Job_ID__NameofCompany')

admin.site.register(Student, StudentAdmin)
admin.site.register(Student_Training_Registration, TrainingRegAdmin)
admin.site.register(Job_Student_Application, JobApplicationAdmin)

admin.site.unregister(SocialAccount)
# admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
# admin.site.unregister(Site)
admin.site.unregister(Group)
# admin.site.unregister(EmailAddress)
# admin.site.unregister(Token)
# if admin.site.is_registered(Job_Student_Application):
#     admin.site.unregister(Job_Student_Application)

# if admin.site.is_registered(Student_Training_Registration):
#     admin.site.unregister(Student_Training_Registration)

# if admin.site.is_registered(Job_Opening):
#     admin.site.unregister(Job_Opening)

# admin.site.register(Student, StudentAdmin)
# admin.site.register(Job_Student_Application)
# admin.site.register(Student_Training_Registration)
# admin.site.register(Job_Opening, JobAdmin)
