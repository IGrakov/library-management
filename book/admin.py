from django.contrib import admin

# Register your models here.
from book.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    list_filter = ('last_name',)
    ordering = ('last_name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    @admin.display(description='Authors')
    def authors(self, book):
        authors = []
        for author_ in book.author.all():
            # join first_name and middle_name only if they are not none
            authors.append(' '.join(filter(None, [author_.last_name, author_.first_name, author_.middle_name])))
        return ', '.join(authors)

    @admin.display(description='Languages')
    def languages(self, book):
        languages = []
        for language in book.language.all():
            languages.append(language.two_letter_code)
        return ', '.join(languages)

    list_display = (
        'title',
        'authors',
        'published_date',
        'isbn',
        'pages',
        'languages',
    )
    list_filter = (
        'title',
        'author',
    )
    ordering = ('title',)
