from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

# Register your models here.
from user.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "is_active", "is_staff")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    @admin.display(description="Groups")
    def group(self, user: User) -> str:
        groups = [group.name for group in user.groups.all()]
        return ", ".join(groups)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "last_name",
                    "first_name",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "last_name",
        "first_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "group",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    ordering = (
        "email",
        "last_name",
    )
