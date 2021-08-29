from django.contrib import admin

from apps.user.models import ParentChildPair, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'name', 'is_child')


admin.site.register(ParentChildPair)
