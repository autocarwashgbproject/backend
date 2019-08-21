from django.shortcuts import render, get_object_or_404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from .models import User, PhoneOTP
from .serializers import CreateUserSerializer, UserDetailSerializer
import random
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import serializers


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
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.delete()
                    user = User.objects.filter(phone__iexact=phone)
                    if user.exists():
                        temp_data = {
                            'username': phone,
                            'password': 'password'
                        }
                        serializer = serializers.AuthTokenSerializer(data=temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.validated_data['user']
                        token, created = Token.objects.get_or_create(user=user)

                        return Response({
                            'ok': True,
                            'id_client': user.id,
                            'is_registered': True,
                            'phone': phone,
                            'token': token.key
                        })
                    else:
                        temp_data = {
                            'phone': phone,
                            'password': 'password'
                        }
                        serializer = CreateUserSerializer(data=temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.set_password(password)
                        user.save()
                        token = Token.objects.create(user=user)

                        return Response({
                            'ok': True,
                            'id_client': user.id,
                            'is_registered': False,
                            'phone': phone,
                            'token': token.key
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
                    'description': "At first go to /api/v1/clients/get_sms/"
                })

        else:
            Response({
                'ok': False,
                'error_code': 452,
                'description': "Phone and/or otp is null"
            })


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    permissoin_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


    def put(self, request, *args, **kwargs):
        client = request.data

        if client['birthday']:
            client['birthday'] = User.format_date_to_base(date = client['birthday'])

        return self.update(request, *args, **kwargs)
