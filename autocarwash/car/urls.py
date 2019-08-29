from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'car'

urlpatterns = [
    path('create/', CarCreateView.as_view()),
    # path('all/', CarListView.as_view()),
    path('<int:pk>/', CarDetailView.as_view()),
]
