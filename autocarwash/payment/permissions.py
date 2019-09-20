from rest_framework import permissions
from re import split
from rest_framework.authtoken.models import Token
from client.models import User
from car.models import Car
from rest_framework.response import Response

# отредактировать TODO
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
            token = split(r' ', token)
            token = token.pop()
        except Exception as e:
            pass
        finally:
            if request.method == "GET":
                pk = view.kwargs['pk']

                try:
                    car = Car.objects.get(id=pk)
                    user = car.user
                    inside_token = Token.objects.get(user=user)

                    if inside_token.key == token:
                        return True
                    else:
                        return False
                    return True

                except Exception as e:
                    return False
            else:
                return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
