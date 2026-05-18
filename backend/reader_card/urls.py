from django.urls import path

from reader_card import views

app_name = "reader_card"

urlpatterns = [
    path("create-reader-card/", views.CreateReaderCardView.as_view(), name="create_reader_card"),
    path("manage-reader-card/<int:pk>/", views.RetrieveUpdateDeleteReaderCardView.as_view(), name="manage_reader_card"),
    path("list-reader-card/", views.ListReaderCardView.as_view(), name="list_reader_card"),
]
