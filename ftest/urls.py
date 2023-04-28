from django.contrib import admin
from django.urls import include, path
from .views import upload_file
from ftest import views
from . import views

urlpatterns = [
    path('upload/', views.upload_file)
]