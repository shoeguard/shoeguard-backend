from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.user.models import Auth, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'name', 'is_parent')


@admin.register(Auth)
class AuthAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'code',
        'is_verified',
    )


api_admin.site.register(User)
api_admin.site.register(Auth)
