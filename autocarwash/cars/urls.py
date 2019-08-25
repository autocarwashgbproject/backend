from django.contrib import admin
from django.urls import path, include
from cars.views import *

app_name = 'cars'

urlpatterns = [
    path('create/', CarCreateView.as_view()),
    path('all/', CarsListView.as_view()),
    path('<int:pk>/', CarsDetailView.as_view()),
]
