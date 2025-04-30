from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'manager')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ( 'email', 'first_name', 'last_name', 'role', 'manager',),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
