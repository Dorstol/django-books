from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomerCreationForm, CustomerChangeForm

Customer = get_user_model()


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]


admin.site.register(Customer, CustomerAdmin)
