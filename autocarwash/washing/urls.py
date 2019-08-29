from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'washing'

urlpatterns = [
    path('', WashingView.as_view()),
]
