from django.urls import path
from . import views

urlpatterns = [

    path('save_resume/', views.save_resume, name='save_resume'),
    path('send-emails/', views.send_emails, name='send_emails'),
    path('email-generator_post/', views.email_generator_post, name='email_generator_post'),
    path('templates/create/', views.create_template_post, name='create_template_post'),
    path('templates/list/', views.create_template_post, name='list_templates'),
    
]

