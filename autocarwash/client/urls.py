from django.urls import path
from .views import ValidatePhoneSendOTP, ValidateOTP, ClientDetailView, \
    LogoutView


app_name = 'client'

urlpatterns = [
    path('sms/', ValidatePhoneSendOTP.as_view()),
    path('register/', ValidateOTP.as_view()),
    path('<int:pk>/', ClientDetailView.as_view()),
    path('<int:pk>/logout/', LogoutView.as_view()),
]
