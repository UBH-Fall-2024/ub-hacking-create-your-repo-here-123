from django.urls import path
from . import views

urlpatterns = [

    path('save_resume/', views.save_resume, name='save_resume'),
]

