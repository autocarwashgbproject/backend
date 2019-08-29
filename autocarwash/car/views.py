from rest_framework import generics
from .serializers import CarDetailSerializer, CarListSerializer
from .models import Car
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication  # Неактивно, так как подключено в настройках
from rest_framework.response import Response


class CarCreateView(generics.CreateAPIView):  # Вьюха создания машины
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwnerOrReadOnly, )
    serializer_class = CarDetailSerializer


class CarListView(generics.ListAPIView):  # Вьюха просмотра всех машин
    serializer_class = CarListSerializer
    queryset = Car.objects.all()  # какие записи вынуть из БД
    permission_classes = (IsAdminUser, )  # Просмотр доступен только если авторизован


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):  # Вьюха просмотра деталей по одной машине
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwnerOrReadOnly, ) # Изменять объект может только пользователь и админ
    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()

    def patch(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        print(int(kwargs['pk']))

        return Response({
            'ok': True,
            'id_car': int(kwargs['pk']),
            'description': "Car was remove"
        })
