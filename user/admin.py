from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    @admin.display(description='Groups')
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ', '.join(groups)

    fieldsets = (
        (None, {'fields': ('password',)}),
        (
            _('Personal info'),
            {
                'fields': (
                    'email',
                    'last_name',
                    'first_name',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    list_display = (
        'email',
        'last_name',
        'first_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'group',
    )
    list_filter = (
        'is_active',
        'is_staff',
    )
    ordering = (
        'email',
        'last_name',
    )
