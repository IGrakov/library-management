from django.contrib import admin

# Register your models here.
from book.models import Book
from user.models import User

admin.site.register(Book)
