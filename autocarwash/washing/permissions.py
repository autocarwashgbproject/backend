from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # сверяем токен в бд у этого пользователя, с токеном, который пришел
        return False
