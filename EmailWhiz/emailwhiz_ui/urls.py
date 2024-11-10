from django.urls import path
from . import views

urlpatterns = [

    path('add_resume/', views.add_resume, name='add_resume'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('view_user_details/', views.view_user_details, name='view_user_details'),
    path('list-resumes/', views.list_resumes, name='list_resumes'),
    path('suggestions-view/', views.suggestions_view, name='suggestions_view'),
    path('email-generator/', views.email_generator, name='email_generator'),
    
    path('select-template/', views.select_template, name='select_template'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('preview-template/', views.preview_template, name='preview_template'),
    
    path('add_employer_details/', views.add_employer_details, name='add_employer_details'),
]

