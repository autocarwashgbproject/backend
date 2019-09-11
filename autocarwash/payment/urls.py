from django.urls import path, re_path
from django.conf.urls import url
from .views import PayCreateView, ResultCreateView

app_name = 'payment'

urlpatterns = [
    path('', PayCreateView.as_view()),
    path('<int:pk>/', ResultCreateView.as_view()),
    
    # re_path(r'^token$',ResultCreateView.as_view()),
]
