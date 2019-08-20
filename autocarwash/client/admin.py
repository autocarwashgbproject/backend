from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import PhoneOTP

admin.site.register(PhoneOTP)

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # Формы для добавления и изменения пользовательского экземпляра
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # Поля, которые будут использоваться при отображении модели пользователя.
    # Они переопределяют определения в базовом UserAdmin.
    # Это ссылки на конкретные поля на auth.User
    list_display = ('name', 'phone', 'admin',)
    list_filter = ('staff', 'active', 'admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')})
    )
    # add_fieldsets не является стандартным атрибутом ModelAdmin.
    # UserAdmin переопределяет get_fieldsets, чтобы использовать этот атрибут при создании пользователя.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}),
    )

    search_fields = ('phone', 'name')
    ordering = ('phone', 'name')
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)

# Удалить групповую модель от администратора. Мы его не используем
admin.site.unregister(Group)
