from django.contrib import admin
from .models import User, UserToken
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = ((None, {'fields': ('email', 'username', 'full_name', 'password', 'last_login')},),
                 (
                     'Permissions', {
                         'fields': ('is_active', 'is_staff', 'is_superuser')},),)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )

    list_display = ('email', 'username', 'full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'full_name', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token_owner', 'token']
    list_display_links = ['id', 'token_owner', 'token']
