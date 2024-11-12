from django.contrib import admin

from reference_values.models import Genre, Hall, Language


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'two_letter_code', 'three_letter_code')
    search_fields = ('name', 'two_letter_code', 'three_letter_code')
    ordering = ('name',)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
