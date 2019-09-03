from django.shortcuts import render
from django.views.generic.edit import CreateView

# Create your views here.

class PayCreateView(CreateView):
    # https://kassa.yandex.ru/developers/payments/recurring-payments
    pass


def wait_url(request): # CreateView
    return render(request, 'payment/index.html')
