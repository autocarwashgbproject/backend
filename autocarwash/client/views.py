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
from rest_framework.authentication import TokenAuthentication


class ValidatePhoneSendOTP(APIView):
    permission_classes = (permissions.AllowAny, )

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
                    return Response({
                        'ok': True,
                        'phone': int(phone),
                        'sms_for_tests': int(key)
                    })
                else:
                    PhoneOTP.objects.create(phone=phone, otp=key, )
                    return Response({
                        'ok': True,
                        'phone': int(phone),
                        'sms_for_tests': int(key)
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
                    password = 'password'
                    if user.exists():
                        temp_data = {
                            'username': phone,
                            'password': password
                        }
                        serializer = serializers.AuthTokenSerializer(data=temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.validated_data['user']
                        token, created = Token.objects.get_or_create(user=user)

                        return Response({
                            'ok': True,
                            'id_client': int(user.id),
                            'is_registered': True,
                            'phone': int(phone),
                            'token': token.key
                        })
                    else:
                        temp_data = {
                            'phone': int(phone),
                            'password': password
                        }
                        serializer = CreateUserSerializer(data=temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.set_password(password)
                        user.save()
                        token = Token.objects.create(user=user)

                        return Response({
                            'ok': True,
                            'id_client': int(user.id),
                            'is_registered': False,
                            'phone': int(phone),
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
    authentication_classes = (TokenAuthentication, )
    permissoin_classes = (permissions.IsAuthenticated, )
    model = User
    queryset = User.objects.all() # TODO сделать фильтр по пк
    serializer_class = UserDetailSerializer
    # slug_field = 'serial'
    # slug_url_kwarg = 'serial'
    # lookup_url_kwarg = 'review_id'
    # def get_queryset(self):
    #     review = self.kwargs['review_id']
    #     return Review.objects.filter(id=review)


    def put(self, request, *args, **kwargs):
        client = request.data

        if client['birthday']:
            try:
                client['birthday'] = User.format_date_to_base(date = client['birthday'])
            except Exception as e:
                return Response({
                    'ok': False,
                    'error_code': 452,
                    'description': "Wrong birthday format, expected Unixtime"
                })

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # TODO что то сделать с клиентом
        client = request.data
        pk = kwargs['pk']

        user = User.objects.filter(id=pk)
        user = user.first()
        token = Token.objects.filter(user=user)
        token_first = token.first()
        token_first.delete()

        return self.destroy(request, *args, **kwargs)



class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.filter(id=pk)
        user = user.first()
        token = Token.objects.filter(user=user)
        token_first = token.first()
        token_first.delete()


        return Response({
            'ok': True,
            'id_client': int(user.id),
            'description': "Token was remove"
        })
