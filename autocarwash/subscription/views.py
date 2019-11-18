from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import render
from .models import Subscription
from .serializers import SubscriptionListSerializer


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionListSerializer
    queryset = Subscription.objects.all()
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        subscription = Subscription.objects.all()
        serializer = SubscriptionListSerializer(subscription, many=True)
        return Response({
            "ok":True,
            "subscription": serializer.data
            })
