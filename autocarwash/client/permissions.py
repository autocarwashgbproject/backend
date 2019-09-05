from rest_framework import permissions
from re import split
from rest_framework.authtoken.models import Token
from client.models import User
from rest_framework.response import Response


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
            token = split(r' ', token)
            token = token.pop()
        except Exception as e:
            pass
        finally:
            pk = view.kwargs['pk']
            try:
                user = User.objects.get(id=pk)
                inside_token = Token.objects.get(user=user)

                if inside_token.key == token:
                    return True
                else:
                    return False
                return True

            except Exception as e:
                return False

    def has_object_permission(self, request, view, obj):
        if obj != 'AnonymousUser':
            return bool(obj.phone == request.user.phone)
        else:
            return False
