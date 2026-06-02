from django.contrib import admin

from book.models import Book, BookCopy


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    @admin.display(description="Authors")
    def authors(self, book: Book) -> str:
        # join first_name and middle_name only if they are not none
        authors = [
            " ".join(filter(None, [author.last_name, author.first_name, author.middle_name]))
            for author in book.author.all()
        ]
        return ", ".join(authors)

    @admin.display(description="Languages")
    def languages(self, book: Book) -> str:
        languages = [language.two_letter_code for language in book.language.all()]
        return ", ".join(languages)

    @admin.display(description="Genres")
    def genres(self, book: Book) -> str:
        genres = [genre.name for genre in book.genre.all()]
        return ", ".join(genres)

    @admin.display(description="Copies")
    def copies(self, book: Book) -> int:
        return BookCopy.objects.filter(book=book).count()

    list_display = (
        "title",
        "authors",
        "published_date",
        "isbn",
        "pages",
        "languages",
        "genres",
        "copies",
    )
    search_fields = ("title",)
    list_filter = (
        "language",
        "genre",
    )
    ordering = ("title",)

    list_per_page = 20


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_select_related = ("book",)
    list_display = (
        "book",
        "uid",
    )
    ordering = (
        "book__title",
        "book__isbn",
        "uid",
    )

    list_per_page = 20
