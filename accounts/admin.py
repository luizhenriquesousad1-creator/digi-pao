from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User


@admin.register(User)

class CostumUserAdmin(UserAdmin):

    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'phone',
                    'is_staff',)


    fieldsets = UserAdmin.fieldsets + (
        ("Informações de contato", {"fields": ("phone",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações de contato", {"fields": ("phone",)}),
    )