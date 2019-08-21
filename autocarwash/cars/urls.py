from django.contrib import admin
from django.urls import path, include
from cars.views import *

app_name = 'car'

urlpatterns = [
    path('car_create/', CarCreateView.as_view()),
    path('all/', CarsListView.as_view()),
    path('car_detail/<int:pk>/', CarsDetailView.as_view()),
]