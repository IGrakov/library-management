from django.contrib import admin

from reference_values.models import Author, Genre, Hall, Language


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "two_letter_code", "three_letter_code")
    search_fields = ("name", "two_letter_code", "three_letter_code")
    ordering = ("name",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name")
    search_fields = ("last_name",)
    ordering = ("last_name",)

    list_per_page = 20
