from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class LoginForm(forms.Form):
    phone = forms.IntegerField(label='Ваш номер телефона')
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Пожалуйста введите проверочный код здесь')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно введите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.object.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError('phone is taken')
        return phone

    def clean_password2(self):
        # Убеждаемся, что обе записи паролей совпадают
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2


class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()


class SetPasswordForm(forms.Form):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно введите пароль', widget=forms.PasswordInput)


class UserAdminCreationForm(forms.ModelForm):
    """
    Форма для создания нового пользователя. Включает в себя все необходимые поля, а также повторный пароль.
    """
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно введите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Убеждаемся, что обе записи паролей совпадают
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        # Сохраняем предоставленный пароль в хешированном формате
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.active = false
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
    Форма для обновления пользователей. Включает в себя все поля пользователя,
    но заменяет поле пароля полем отображения пароля хэша администратора
    """
    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        # Независимо от того, что предоставляет пользователь, верните начальное значение.
        # Это делается здесь, а не на поле, потому что поле значения
        # не имеет доступа к начальному значению
        return self.initial['password']
