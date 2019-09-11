from django.contrib import admin
from .models import BankUsers, OrderBankUsers, CardBankUsers
# Register your models here.
admin.site.register(BankUsers)
admin.site.register(OrderBankUsers)
admin.site.register(CardBankUsers)
