from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import CreateWashingSerializer
from car.models import Car, SubscriptionCar
from rest_framework.views import APIView
from .models import Washing
# Create your views here.

class WashingCreateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        reg_num = request.data.get('reg_num')
        wash = 1 # пока одна мойка

        if reg_num:
            car = Car.objects.filter(reg_num=reg_num)
            if car.exists():
                data = request.data
                data['wash'] = wash
                car_id = [car.id for car in car]

                data['car'] = car_id[0]

                if SubscriptionCar.is_active_sub(car):
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
            # нету номера машины
            return Response({
                "ok": False,
                'error_code': 404,
                'description': "We can't see a reg_num"
            })


class WashingDetailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        washing = Washing.objects.filter(car=kwargs['pk'])
        serializer = CreateWashingSerializer(washing, many=True)
        
        return Response(serializer.data)
