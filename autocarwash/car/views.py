from rest_framework import generics
from .serializers import CarDetailSerializer, CarListSerializer
from .models import Car
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication  # Неактивно, так как подключено в настройках


class CarCreateView(generics.CreateAPIView):  # Вьюха создания машины
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )
    serializer_class = CarDetailSerializer


class CarListView(generics.ListAPIView):  # Вьюха просмотра всех машин
    serializer_class = CarListSerializer
    queryset = Car.objects.all()  # какие записи вынуть из БД
    permission_classes = (IsAdminUser, )  # Просмотр доступен только если авторизован


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):  # Вьюха просмотра деталей по одной машине
    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )  # Изменять объект может только пользователь и админ
