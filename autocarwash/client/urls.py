from django.urls import path, include
from knox import views as knox_views
from .views import ValidatePhoneSendOTP, ValidateOTP, ClientDetailView

app_name = 'client'

urlpatterns = [
    # register a validate_phone: str
    path('get_sms/', ValidatePhoneSendOTP.as_view()),
    path('register/', ValidateOTP.as_view()),
    path('<int:pk>/', ClientDetailView.as_view()),
    # path('loqout/', LogoutView.as_view()),
]
