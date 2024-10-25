from django.contrib import admin

# Register your models here.
from book.models import Author, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    list_filter = ('last_name',)
    ordering = ('last_name',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
