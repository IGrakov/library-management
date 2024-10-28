from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    @admin.display(description='Groups')
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

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
        'last_name',
        'email',
    )
    ordering = (
        'last_name',
        'email',
    )
