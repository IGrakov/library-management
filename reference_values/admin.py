from django.contrib import admin

# Register your models here.
from reference_values.models import Genre, Language

admin.site.register(Language)
admin.site.register(Genre)
