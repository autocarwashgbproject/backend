from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'washing'

urlpatterns = [
    path('create/', WashingCreateView.as_view()),
    path('<int:pk>/', WashingDetailView.as_view()),
]
