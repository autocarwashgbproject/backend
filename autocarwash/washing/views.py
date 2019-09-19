from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, generics
from .serializers import CreateWashingSerializer
from car.models import Car, SubscriptionCar, sub_date_plus_month
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
            cars = Car.objects.filter(reg_num=reg_num)
            car = cars.first()
            car_id = car.id
            user = car.user_id

            data = request.data
            data['user'] = user

            if cars.exists():
                data['wash'] = wash
                data['car'] = car_id
                subscription_dates = SubscriptionCar.objects.filter(reg_num = car_id).order_by('-subscription_date')

                if subscription_dates.exists():
                    subscription_date = subscription_dates.first().subscription_date
                    plus_month = sub_date_plus_month(subscription_date)
                    if SubscriptionCar.is_subscribe(plus_month):
                        washings = Washing.objects.filter(car = car_id).order_by('-timestamp')
                        if washings.exists():
                            washings = washings.first()
                            washings = washings.timestamp
                            if Washing.is_washing_today(washings) == False:
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
                                data['washing'] = "Arleady washing today"
                                serializer = CreateWashingSerializer(data=data)
                                serializer.is_valid(raise_exception=True)
                                washing = serializer.save()
                                washing.save()

                                return Response({
                                    "ok": False,
                                    'description': "Arleady washing today"
                                })
                        else:
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
        pk = kwargs['pk']
        washing = Washing.objects.filter(user=pk)

        serializer = CreateWashingSerializer(washing, many=True)

        return Response({
            "ok":True,
            "washing": serializer.data
        })
