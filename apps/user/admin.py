from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.user.models import Auth, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'name', 'is_parent')


admin.site.register(Auth)

api_admin.site.register(User)
api_admin.site.register(Auth)
