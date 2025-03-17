from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Unite

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'unite', 'is_employee', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('unite', 'is_employee', 'is_superuser')}),
    )

admin.site.register(Unite)
