from django.urls import path, re_path
from django.conf.urls import url
from .views import PayCreateView, ResultCreateView, PaymentDetailView, CardsDetailView

app_name = 'payment'

urlpatterns = [
    path('', PayCreateView.as_view()),
    path('<int:pk>/', ResultCreateView.as_view()),
    path('history/<int:pk>/', PaymentDetailView.as_view()), # user pk
    path('cards/<int:pk>/', CardsDetailView.as_view()), # user pk

    # re_path(r'^token$',ResultCreateView.as_view()),
]
