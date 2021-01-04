from django.contrib import admin
from django.urls import path, re_path, include
from students import views
from students.views import *
from django.conf.urls import url

urlpatterns = [
    path('', students_list, name='students_list'),
    path('api/students/', students_list, name='students_list'),
    path('api/students/<pk>', students_detail, name='students_detail'),
]