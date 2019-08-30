from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, generics
from .serializers import CreateWashingSerializer
from car.models import Car, SubscriptionCar
from rest_framework.views import APIView
from .models import Washing
from .permissions import IsOwner
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class WashingCreateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        reg_num = request.data.get('reg_num')
        wash = 1 # пока одна мойка
        pay = request.data.get('pay')

        if reg_num and len(reg_num)<=9:
            car = Car.objects.filter(reg_num=reg_num)
            if car.exists():
                data = request.data
                data['wash'] = wash
                car_id = [car.id for car in car]

                data['car'] = car_id[0]
                if pay: #TODO (для тестов) SubscriptionCar.is_active_sub(car):
                    # TODO Добавить проверку на помывку на 1 раз в сутки
                    data['washing'] = "Success"

                    serializer = CreateWashingSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    washing = serializer.save()
                    washing.save()

                    return Response({
                        "ok": True,
                        'description': "Washing"
                    })

                else:
                    # не активна подписка
                    data['is_active'] = False
                    data['washing'] = "No subscription"

                    serializer = CreateWashingSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    washing = serializer.save()
                    washing.save()

                    return Response({
                    "ok": False,
                    'error_code': 403,
                    'description': "No subscription"
                })

            else:
                # машина не существует
                return Response({
                "ok": False,
                'error_code': 404,
                'description': "There is no reg_num in database"
            })

        else:
            # нету номера машины или длина больше
            return Response({
                "ok": False,
                'error_code': 404,
                'description': "Wrong reg_num, format А001АА777, max 9 symbols"
            })


class WashingDetailView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwner, )

    def get(self, request, *args, **kwargs):

        washing = Washing.objects.objects.filter(user=kwargs['pk'])

        serializer = CreateWashingSerializer(washing, many=True)

        return Response(serializer.data)
