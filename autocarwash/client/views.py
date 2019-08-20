from django.shortcuts import render, get_object_or_404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from .models import User, PhoneOTP
from .serializers import CreateUserSerializer, LoginSerializer, UserSerializer
import random
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        tel_num = request.data.get('phone')
        if tel_num:
            phone = str(tel_num)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    # если прошли сутки то обновляем до 0 count в PhoneOTP
                    # то есть надо запоминать когда был запрос и сохранять в бд PhoneOTP

            key = send_otp(phone)
            if key:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    count = old.count
                    if count > 10:
                        return Response({
                            'ok': False,
                            'error_code': 403,
                            'description': "It's too many attempts, connect with support"
                        })
                    old.count = count + 1
                    old.otp = key
                    old.save()
                    print('увеличение значения', count)
                    return Response({
                        'ok': True,
                        'error_code': 200,
                        'description': "We send sms",
                        'phone': phone,
                        'sms_for_tests': key
                    })
                else:
                    PhoneOTP.objects.create(phone=phone, otp=key, )
                    return Response({
                        'ok': True,
                        'error_code': 200,
                        'description': "We send sms",
                        'phone': phone,
                        'sms_for_tests': key
                    })
            else:
                return Response({
                    'ok': False,
                    'error_code': 404,
                    'description': "We can't send sms, please, connect with support"
                })
        else:
            return Response({
                'ok': False,
                'error_code': 404,
                'description': "We can't send sms, please, connect with support"
            })


def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        print(key)
        return key
    else:
        return False


class ValidateOTP(APIView):
    """
    Если вы получили проверочный код (otp), отправьте запрос по телефону, и вы будете перенаправлены для ввода пароля
    """
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    # сгенерировать пароль
                    # создать клиента
                    # выдать ответ с ид, номером и т д
                    return Response({
                        'ok': True,
                        'error_code': 200,
                        'description': "Next step is registration"
                    })

                else:
                    return Response({
                        'ok': False,
                        'error_code': 452,
                        'description': "Wrong otp"
                    })

            else:
                Response({
                    'ok': False,
                    'error_code': 404,
                    'description': "At first go to /api/v1/clients/validate_phone/"
                })

        else:
            Response({
                'ok': False,
                'error_code': 452,
                'description': "Phone and/or otp is null"
            })


class Register(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'phone': phone,
                        'password': password
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    user.set_password(password)
                    user.save()
                    old.delete() # TODO
                    return Response({
                        'ok': False,
                        'error_code': 200,
                        'description': "Client was created",
                        'phone': phone
                    })
                else:
                    return Response({
                        'ok': False,
                        'error_code': 452,
                        'description': "Not validated, please go to /api/v1/clients/validate_otp/"
                    })

            else:
                Response({
                    'ok': False,
                    'error_code': 452,
                    'description': "No such phone, please go to /api/v1/clients/validate_phone/"
                })

        else:
            Response({
                'ok': False,
                'error_code': 452,
                'description': "Phone and/or otp is null"
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
