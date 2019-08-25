from rest_framework import generics
from cars.serializers import CarDetailSerializer, CarsListSerializer
from cars.models import Car
from cars.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication  # Неактивно, так как подключено в настройках


class CarCreateView(generics.CreateAPIView):  # Вьюха создания машины
    serializer_class = CarDetailSerializer


class CarsListView(generics.ListAPIView):  # Вьюха просмотра всех машин
    serializer_class = CarsListSerializer
    queryset = Car.objects.all()  # какие записи вынуть из БД
    permission_classes = (IsAuthenticated, )  # Просмотр доступен только если авторизован


class CarsDetailView(generics.RetrieveUpdateDestroyAPIView):  # Вьюха просмотра деталей по одной машине
    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )  # Изменять объект может только пользователь и админ
# IsOwnerOrReadOnly,
