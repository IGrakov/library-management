from django.urls import path

from book import views

app_name = "book"

urlpatterns = [
    path("create-book/", views.CreateBookView.as_view(), name="create_book"),
    path("manage-book/<int:pk>/", views.RetrieveUpdateDeleteBookView.as_view(), name="manage_book"),
    path("list-book/", views.ListBookView.as_view(), name="list_book"),
    path("create-author/", views.CreateAuthorView.as_view(), name="create_author"),
    path("manage-author/<int:pk>/", views.RetrieveUpdateDeleteAuthorView.as_view(), name="manage_author"),
    path("list-author/", views.ListAuthorView.as_view(), name="list_author"),
    path("create-book-copy/", views.CreateBookCopyView.as_view(), name="create_book_copy"),
    path("manage-book-copy/<int:pk>/", views.RetrieveDeleteBookCopyView.as_view(), name="manage_book_copy"),
    path("list-book-copy/", views.ListBookCopyView.as_view(), name="list_book_copy"),
    path("test-queries/", views.testView, name="test_queries"),
]
