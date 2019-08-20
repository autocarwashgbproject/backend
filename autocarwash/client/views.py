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
                return Response({
                    'status': False,
                    'detail': 'Номер телефона уже существует'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'detail': 'Ошибка отправки проверочного кода. Превышен лимит, обратитесь в поддержку'
                            })
                        old.count = count + 1
                        old.save()
                        print('увеличение значения', count)
                        return Response({
                            'status': True,
                            'detail': 'Проверочный код успешно отправлен'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        return Response({
                            'status': True,
                            'detail': 'Проверочный код успешно отправлен'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Ошибка отправки проверочного кода'
                    })


        else:
            return Response({
                'status': False,
                'detail': 'Номер телефона не указан в запросе'
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
                    return Response({
                        'status': True,
                        'detail': 'Проверочный код (OTP) совпал. Пожалуйста, перейдите к регистрации'
                    })

                else:
                    return Response({
                        'status': False,
                        'detail': 'Проверочный код (OTP) не верный'
                    })

            else:
                Response({
                    'status': False,
                    'detail': 'Сначала выполните отправку запроса проверочного кода (OTP)'
                })

        else:
            Response({
                'status': False,
                'detail': 'Пожалуйста, предоставьте номер телефон, а также проверочный код (otp) для проверки'
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
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Аккаунт создан'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Проверочный код (OTP) не подтвержден. Сначала подтвердите.'
                    })

            else:
                Response({
                    'status': False,
                    'detail': 'Пожалуйста, сначала проверьте телефон'
                })

        else:
            Response({
                'status': False,
                'detail': 'Телефон и пароль не отправляются'
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
