from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .serializers import CreateWashingSerializer
from car.models import Car, SubscriptionCar

# Create your views here.

class WashingCreateView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        reg_num = request.data.get('reg_num')
        wash = 1 # пока одна мойка

        if reg_num:
            car = Car.objects.filter(reg_num=reg_num)
            if car.exists()
                data = request.data
                data['wash'] = wash
                car_id = [car.id for car in cars]
                data['car'] = car_id.first()

                if SubscriptionCar.is_active_sub(car):
                    data['washing'] = "No subscription"

                    serializer_class = CreateWashingSerializer

                    return Response({
                        "ok": true,
                        'error_code': 200,
                        'description': "Washing"
                    })

                else:
                    # не активна подписка
                    data['is_active'] = False
                    data['washing'] = "No subscription"

                    serializer_class = CreateWashingSerializer

                    return Response({
                    "ok": false,
                    'error_code': 403,
                    'description': "No subscription"
                })

            else:
                # машина не существует
                return Response({
                "ok": false,
                'error_code': 404,
                'description': "There is no reg_num in database"
            })

        else:
            # нету номера машины
            serializer_class = CreateWashingSerializer
            return Response({
                "ok": false,
                'error_code': 404,
                'description': "We can't see a reg_num"
            })
