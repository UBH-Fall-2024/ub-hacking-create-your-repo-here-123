from django.urls import path
from . import views

urlpatterns = [

    path('save_resume/', views.save_resume, name='save_resume'),
    path('send-emails/', views.send_emails, name='send_emails'),
    path('email-generator_post/', views.email_generator_post, name='email_generator_post'),
]

