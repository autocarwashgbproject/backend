from rest_framework import permissions
from re import split
from rest_framework.authtoken.models import Token
# from .models import


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print()
        print(obj.phone)
        print(type(obj.phone))
        print()
        print(request.user.phone)
        print(type(request.user.phone))
        print()
        return bool(obj.phone == request.user.phone)
