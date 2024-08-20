from django.urls import path

from book import views

app_name = 'book'

urlpatterns = [
    path('create-book/', views.CreateBookView.as_view(), name='create_book'),
    path('manage-book/<int:pk>/', views.RetrieveUpdateDeleteBookView.as_view(), name='manage_book'),
    path('list-book/', views.ListBookView.as_view(), name='list_book'),
]
