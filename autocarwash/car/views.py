from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .serializers import CarDetailSerializer, CarListSerializer
from .models import Car
from .permissions import IsOwner


class CarCreateView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwner, )
    serializer_class = CarDetailSerializer


class CarListView(generics.ListAPIView):
    serializer_class = CarListSerializer
    queryset = Car.objects.all()
    permission_classes = (IsAdminUser, )


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwner, )
    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()

    def patch(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            'ok': True,
            'id': int(kwargs['pk']),
            'description': "Car was remove"
        })
