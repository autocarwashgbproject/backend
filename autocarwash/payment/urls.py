from django.urls import path
from .views import UrlPayCreateView

app_name = 'payment'

urlpatterns = [
    # register a validate_phone: str
    path('', UrlPayCreateView.as_view()),
    path('<int:pk>/', Payment.as_view()),
]
