from django.urls import path
from . import views

urlspatterns=[
    path('',views.dashboard,name='dashboard')
]