from django.urls import path, include
from knox import views as knox_views
from .views import ValidatePhoneSendOTP, ValidateOTP, Register, LoginAPI, ClientDetailView

app_name = 'client'

urlpatterns = [
    # register a validate_phone: str
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
    path('login/', LoginAPI.as_view()),
    path('loqout/', knox_views.LogoutView.as_view()),
    path('<int:pk>/', ClientDetailView.as_view()),
]
