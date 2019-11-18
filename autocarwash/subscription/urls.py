from django.urls import path
from .views import *


app_name = 'subscription'

urlpatterns = [
    path('all/', SubscriptionListView.as_view()),
]
