from django.contrib import admin

# Register your models here.
from reference_values.models import Genre, Language


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
