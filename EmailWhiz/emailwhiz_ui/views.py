
# EmailWhiz/emailwhiz_ui/views.py
from django.shortcuts import redirect, render
from django.conf import settings
import os
from PyPDF2 import PdfReader
import requests
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User

from emailwhiz_api.views import get_user_details
from emailwhiz_ui.forms import CustomUserCreationForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from emailwhiz_ui.forms import CustomUserCreationForm


def suggestions_view(request):
    suggestions = [
        {"first_name": "Alice", "last_name": "Johnson", "organization_email_id": "alice.johnson@aws.com", "organization": "Amazon"},
        {"first_name": "Bob", "last_name": "Smith", "organization_email_id": "bob.smith@aws.com", "organization": "Amazon"},
        {"first_name": "Carol", "last_name": "Davis", "organization_email_id": "carol.davis@aws.com", "organization": "Amazon"},
        {"first_name": "David", "last_name": "Wilson", "organization_email_id": "david.wilson@aws.com", "organization": "Amazon"},
        {"first_name": "Eve", "last_name": "Miller", "organization_email_id": "eve.miller@aws.com", "organization": "Amazon"}
    ]
    
    return render(request, 'suggestions.html', {'suggestions': suggestions})

def add_employer_details(request):
    resume = request.GET.get('resume')
    if not resume:
        # If the parameter is missing, return a 400 Bad Request response
        return HttpResponseBadRequest('Missing required query parameter: param1')

    body = {"resume": resume}
    return render(request, 'email_generator.html', body)


def view_generated_emails(request, data):
    # body = json.loads(request.body)
    # print(data)
    body = {
        "data": [{
            "first_name": "firstName",
            "last_name": "lastName",
            "email": "email",
            "company": "company",
            "job_role": "jobRole",
            "email_content": "email_content"
        },
        ]
    }
    return render(request, 'view_generated_emails.html', body)

def view_user_details(request):
    details = get_user_details(request.user)
    print("Details: ", details)
    if details['graduation_done'] == True:
        details['graduation_done'] = 'Yes'
    else:
        details['graduation_done'] = 'No'
    resumes_dir = os.path.join(settings.BASE_DIR, 'emailwhiz_api', 'users', details['username'], 'resumes')
    print("resume_dir: ", resumes_dir, settings.BASE_DIR)
    resumes = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    print("resumes: ", resumes)
    return render(request, 'view_user_details.html', {'details': details,  'username': details['username'],  'resumes': resumes})

def home(request):
    details = get_user_details(request.user)
    upload_dir = os.path.join(settings.MEDIA_ROOT, f'{details["username"]}/resumes')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return render(request, 'base.html')

def list_resumes(request):
    details = get_user_details(request.user)
    username = details['username']  # Placeholder: Replace with the actual user's email
    print("username:", username)
    resumes_dir = os.path.join(settings.BASE_DIR, 'emailwhiz_api', 'users', username, 'resumes')
    print("resume_dir: ", resumes_dir, settings.BASE_DIR)
    resumes = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    print("resumes: ", resumes)
    return render(request, 'list_resumes.html', {'resumes': resumes, 'username': username})

def select_template(request):
    details = get_user_details(request.user)
    username = details['username']
    templates_dir = os.path.join(settings.BASE_DIR, 'emailwhiz_api', 'users', username, 'templates')
    
    first_email_templates = os.listdir(os.path.join(templates_dir, 'first_email'))
    followup_email_templates = os.listdir(os.path.join(templates_dir, 'followup_email'))
    
    context = {
        'first_email_templates': first_email_templates,
        'followup_email_templates': followup_email_templates
    }
    return render(request, 'emailwhiz_ui/select_template.html', context)


def upload_excel(request, user):
    if request.method == "POST":
        excel_file = request.FILES['excel']
        # Process Excel data and render table
        request.session['excel_data'] = ...  # Save processed data in session for preview
        return redirect('preview_template', user=user)
    return render(request, 'myapp/upload_excel.html')

def preview_template(request, user):
    selected_resume = request.session.get('selected_resume')
    selected_template = request.session.get('selected_template')
    excel_data = request.session.get('excel_data')
    if request.method == "POST":
        # Send the email here
        return redirect('success_page')
    return render(request, 'myapp/preview_template.html', {
        'resume': selected_resume,
        'template': selected_template,
        'excel_data': excel_data,
    })


def email_generator(request):
    resume = request.POST.get('selected_resume')
    return render(request, 'email_generator.html', {"resume":resume})
    



def add_resume(request):
    return render(request, 'add_resume.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to the name of the view or URL where you want to redirect on successful login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            # Display error messages if form is not valid
            messages.error(request, "Please fix the errors below.")
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()  # Instantiate an empty form for GET request
    return render(request, 'register.html', {'form': form})

def add_employer_details(request):
    # body = json.loads(request.body)
    body = {"resume": "abcd"}
    return render(request, 'email_generator.html', body)

