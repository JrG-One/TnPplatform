from django.contrib.staticfiles import finders
from fpdf import FPDF
import fpdf
import io
from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from google.oauth2.credentials import Credentials

from inspect import getsourcefile
from django.conf import settings
from os.path import abspath
from pathlib import Path
import os


fpdf.set_global("FPDF_CACHE_MODE", 1)
def generate_pdf(data):
    pdf = FPDF('P', 'mm', 'Letter') # Page size
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=7)
    
    # font_path = abspath('cmr12.ttf')
    # print(font_path)  

    font_path1 = os.path.join(settings.BASE_DIR, 'student', 'fonts', 'cmr12.ttf')
    font_path2 = os.path.join(settings.BASE_DIR, 'student', 'fonts', 'cmbx12.ttf')
    font_path3 = os.path.join(settings.BASE_DIR, 'student', 'fonts', 'cmsl12.ttf')
    image_path1 = os.path.join(settings.BASE_DIR, 'student', 'images', 'phone-flip-solid.png')
    image_path2 = os.path.join(settings.BASE_DIR, 'student', 'images', 'envelope-solid.png')
    image_path3 = os.path.join(settings.BASE_DIR, 'student', 'images', 'github.png')
    image_path4 = os.path.join(settings.BASE_DIR, 'student', 'images', 'linkedin.png')
    pdf.add_font('cmr', '', font_path1, uni = True)
    pdf.add_font('cmbx','', font_path2, uni = True)
    pdf.add_font('cmsl','', font_path3, uni = True)

    pdf.set_font("cmr", "", 24) 
    remain_space = 204 - pdf.get_x()
    pdf.cell(0, 7, data["Name"] , ln=1, align="C")

    pdf.set_font("cmr", "", 10)
    if data.get('mobile'):
        pdf.set_x(pdf.get_x() + 60)
        pdf.image(image_path1, x=pdf.get_x(), y=pdf.get_y()+1, w=3.5, h=3.2)
        pdf.set_x(pdf.get_x() + 4)
        width = pdf.get_string_width(data['mobile'])
        pdf.cell(width + 2, 5, data['mobile']) 

        
    pdf.set_font("cmr", "U", 10) 
    if data.get('email'):  
        pdf.set_x(pdf.get_x() + 2)
        pdf.image(image_path2, x=pdf.get_x(), y=pdf.get_y()+1, w=3.5, h=3.5)      
        pdf.set_x(pdf.get_x() + 4)
        pdf.set_link(link=f"mailto:{data['email']}")
        width = pdf.get_string_width(data['email'])
        pdf.cell(width+2, 5, data['email'], ln=1)
        pdf.set_link(link='')

    if data.get('linked'):
        pdf.set_x(pdf.get_x() + 50)
        pdf.image(image_path4, x=pdf.get_x(), y=pdf.get_y()+1, w=3.5, h=3.5)
        pdf.set_x(pdf.get_x() + 4)
        width = pdf.get_string_width(data['linked'])
        linkedin = f"https://{data['linked']}"
        pdf.cell(width + 2, 5, data['linked'],link=linkedin)
        
        
    if data.get('github'):
        pdf.set_x(pdf.get_x() + 2)
        pdf.image(image_path3, x=pdf.get_x(), y=pdf.get_y()+1, w=3.5, h=3.5)
        pdf.set_x(pdf.get_x() + 4)
        width = pdf.get_string_width(data['github'])
        github = f"https://{data['github']}"
        pdf.cell(width + 2, 5, data['github'], ln=1,link=github)
        pdf.set_link(link='')

    if data.get('CareerSum'):
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Career summary so far", ln=1)
        pdf.set_line_width(0.2)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        pdf.set_y(pdf.get_y() + 1)
        pdf.set_font("cmr", "", 10)

        remain_space = 204 - pdf.get_x()
        lines = pdf.multi_cell(remain_space, 5, data['CareerSum'].get("data"))

        for line in lines:
            pdf.cell(0, 5, line)

        pdf.set_y(pdf.get_y() + 2)

    # Check if 'education' key exists
    if data.get('education'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, 'Education', ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        pdf.set_font("cmbx", "", 12)
        pdf.cell(0, 7, "Secondary Education :", ln=1)
        pdf.set_font("cmbx", "", 11)
        pdf.cell(0, 6, data['tenth'].get("tenth_name"))
        pdf.cell(0, 6, data['tenth'].get("tenth_period"), ln=1, align="R")
        pdf.cell(0, 6, "Grade : " + data['tenth'].get("tenth_per"), ln=1)
        pdf.set_font("cmsl", "", 10)
        lines = pdf.multi_cell(remain_space, 4, data['tenth'].get("tenth_details"))
        
        for line in lines:
            pdf.cell(0, 5, line)
        
        pdf.set_font("cmbx", "", 12)
        pdf.cell(0, 7, "Higher Secondary Education :", ln=1)
        pdf.set_font("cmbx", "", 11)
        pdf.cell(0, 6, data['twelth'].get("twelth_name"))
        pdf.cell(0, 6, data['twelth'].get("twelth_period"), ln=1, align="R")
        pdf.cell(0, 6, "Grade : " + data['twelth'].get("twelth_per"), ln=1)
        pdf.set_font("cmsl", "", 10)
        lines = pdf.multi_cell(remain_space, 4, data['twelth'].get("twelth_details"))
        
        for line in lines:
            pdf.cell(0, 5, line)
            
        pdf.set_font("cmbx", "", 12)
        pdf.cell(0, 7, "Institute Education :", ln=1)
        pdf.set_font("cmbx", "", 11)
        pdf.cell(0, 6, data['education'].get("Education_clg"))
        pdf.cell(0, 6, data['education'].get("ed_date"), ln=1, align="R")
        pdf.cell(0, 6, "CGPA : " + data['education'].get("ins_cgpa"), ln=1)
        pdf.set_font("cmsl", "", 10)
        lines = pdf.multi_cell(remain_space, 4, data['education'].get("edu_details"))

        for line in lines:
            pdf.cell(0, 5, line)
        pdf.set_y(pdf.get_y() + 2)

    # Check if 'achievement' key exists
    if data.get('achievement'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Achievements", ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_font("cmr", "", 10)
        for i in range(len(data["achievement"])):
            pdf.cell(3)
            lines = pdf.multi_cell(remain_space, 4, data['achievement'][i].get("ach_details"))
            
            for line in lines:
                pdf.cell(0, 5, line)
            pdf.set_y(pdf.get_y() + 1)
        pdf.set_y(pdf.get_y() + 2)

    # Check if 'experience' key exists
    if data.get('experience'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Experience", ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        for i in range(len(data['experience'])):
            pdf.set_font("cmbx", "", 11)
            pdf.cell(0, 6, data['experience'][i].get("exp_company"))
            pdf.cell(0, 6, data['experience'][i].get("exp_date"), ln=1, align="R")
            pdf.set_font("cmr", "", 10)
            pdf.cell(0, 5, data['experience'][i].get("exp_details1"))
            pdf.cell(0, 5, data['experience'][i].get("exp_details2"), ln=1, align="R")
            for j in range(len(data['experience'][i].get("exp_details3"))):
                pdf.cell(3)
                pdf.multi_cell(remain_space, 4, data['experience'][i].get("exp_details3")[j].get("exp_details"))
                
                for line in lines:
                    pdf.cell(0, 5, line)
        pdf.set_y(pdf.get_y() + 2)

    # Check if 'Internships' key exists
    if data.get('Internships'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Internships", ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        for i in range(len(data['Internships'])):
            pdf.set_font("cmbx", "", 11)
            pdf.cell(0, 6, data['Internships'][i].get("intern_company"))
            pdf.cell(0, 6, data['Internships'][i].get("intern_date"), ln=1, align="R")
            pdf.set_font("cmr", "", 10)
            pdf.cell(0, 5, data['Internships'][i].get("intern_details1"))
            pdf.cell(0, 5, data['Internships'][i].get("intern_details2"), ln=1, align="R")
            for j in range(len(data['Internships'][i].get("intern_details3"))):
                pdf.cell(3)
                pdf.multi_cell(remain_space, 4, data['Internships'][i].get("intern_details3")[j].get("intern_details"))
                for line in lines:
                    pdf.cell(0, 5, line)
        pdf.set_y(pdf.get_y() + 2)

    # Check if 'Hackathon' key exists
    if data.get('Hackathon'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Hackathons Won", ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        for i in range(len(data['Hackathon'])):
            pdf.set_font("cmbx", "", 11)
            pdf.cell(0, 6, data['Hackathon'][i].get("hack_title"))
            pdf.cell(0, 6, data['Hackathon'][i].get("hack_date"), ln=1, align="R")
            pdf.set_font("cmr", "", 10) 
            for j in range(len(data['Hackathon'][i].get("hack_details"))):
                pdf.cell(3)
                lines = pdf.multi_cell(remain_space, 4, data['Hackathon'][i].get("hack_details")[j].get("hack_details1"))
                for line in lines:
                    pdf.cell(0, 5, line)
        pdf.set_y(pdf.get_y() + 2)

    # Check if 'Gitproj' key exists
    if data.get('Gitproj'):
        pdf.set_font("cmbx", "", 14)
        pdf.cell(0, 7, "Notable Github Projects", ln=1)
        pdf.line(10, pdf.get_y(), 204, pdf.get_y())
        for i in range(len(data['Gitproj'])):
            pdf.set_font("cmbx", "", 11)
            lines = pdf.multi_cell(remain_space, 6, data['Gitproj'][i].get("gitproj_title"))

            for line in lines:
                pdf.cell(0, 5, line)

            pdf.set_font("cmr", "", 10)
            for j in range(len(data['Gitproj'][i].get("gitproj_details"))):
                pdf.cell(3)
                lines = pdf.multi_cell(remain_space, 4, data['Gitproj'][i].get("gitproj_details")[j].get("gitproj_details1"))

                for line in lines:
                    pdf.cell(0, 5, line)
    # print(f"Output file: {output_file}")
    # pdf.output(output_file, "F")
    # print("PDF generated")
    pdf_data = pdf.output(dest='S').encode('latin1')
    # print("PDF generated")

    return pdf_data

def store_pdf_in_drive(user, pdf_content, file_name='document.pdf'):
    credentials = get_google_drive_credentials(user)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': file_name,
        'mimeType': 'application/pdf'
    }

    media = MediaIoBaseUpload(io.BytesIO(pdf_content), mimetype='application/pdf')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    # web_view_link = file.get('webViewLink')

    permission_all = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_id, body = permission_all).execute()
    return file_id
    # return file.get('id')

def get_google_drive_credentials(user):
    try:
        # Retrieve the SocialAccount linked to the user's Google account
        google_social_account = SocialAccount.objects.get(provider='google', user=user)

        google_social_token = SocialToken.objects.get(account=google_social_account)
        # print(google_social_token.token)
        # print(google_social_token.token_secret)
        # Access the Google Drive credentials
        social_app = SocialApp.objects.get(provider='google')
        credentials_data = {
            'token': google_social_token.token,
            'refresh_token': google_social_token.token_secret,  # Assuming refresh_token is stored here
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': social_app.client_id,
            'client_secret': social_app.secret,
            'scopes': ['https://www.googleapis.com/auth/drive.file'],
        }
        credentials = Credentials.from_authorized_user_info(credentials_data)

        # You can now use 'credentials' to interact with Google Drive API
        return credentials

    except SocialAccount.DoesNotExist:
        # Handle the case where the user is not connected with Google
        return None
 
