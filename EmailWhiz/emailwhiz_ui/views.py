
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from emailwhiz_ui.forms import CustomUserCreationForm

def add_resume(request):
    return render(request, 'add_resume.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('resume_form')  # Change 'home' to the name of the view or URL where you want to redirect on successful login
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

