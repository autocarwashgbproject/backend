from django.urls import path
from .views import *


app_name = 'car'

urlpatterns = [
    path('', CarCreateView.as_view()),
    # path('all/', CarListView.as_view()),
    path('<int:pk>/', CarDetailView.as_view()),
]
