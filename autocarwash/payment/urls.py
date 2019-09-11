from django.urls import path
from .views import PayCreateView

app_name = 'payment'

urlpatterns = [
    path('', PayCreateView.as_view()), # сразу так сделать, что бы передавать ид машины по которой оплата, а далее мы средиректим на страницу авторизации paymaster по auth доступу
]
