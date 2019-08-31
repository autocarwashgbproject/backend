from django.shortcuts import render
from django.views.generic.edit import CreateView
from rest_framework import generics

# Create your views here.

class UrlPayCreateView(generics.CreateAPIView):
    pass


class Payment(CreateView):
    pass
