from django.shortcuts import render
from rest_framework import generics
from .models import Subscription
from rest_framework.permissions import AllowAny

# Create your views here.

class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionListSerializer
    queryset = Subscription.objects.all()
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        subscription = Subscription.objects.all()

        serializer = SubscriptionListSerializer(washing, many=True)

        return Response({
            "ok":True,
            "subscription": serializer.data
        })
