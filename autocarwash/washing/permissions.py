from rest_framework import permissions
from re import split
from rest_framework.authtoken.models import Token
from client.models import User
# from .models import


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers['Authorization']
        token = split(r' ', token)
        token = token.pop()
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
        return bool(obj.phone == request.user.phone)
