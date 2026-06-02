from django.urls import path

from reference_values import views

app_name = "reference_values"

urlpatterns = [
    path("add-language/", views.CreateLanguageView.as_view(), name="add_language"),
    path("manage-language/<int:pk>/", views.RetrieveUpdateDeleteLanguageView.as_view(), name="manage_language"),
    path("list-language/", views.ListLanguageView.as_view(), name="list_language"),
    path("add-genre/", views.CreateGenreView.as_view(), name="add_genre"),
    path("manage-genre/<int:pk>/", views.RetrieveUpdateDeleteGenreView.as_view(), name="manage_genre"),
    path("list-genre/", views.ListGenreView.as_view(), name="list_genre"),
    path("add-hall/", views.CreateHallView.as_view(), name="add_hall"),
    path("manage-hall/<int:pk>/", views.RetrieveUpdateDeleteHallView.as_view(), name="manage_hall"),
    path("list-hall/", views.ListHallView.as_view(), name="list_hall"),
    path("add-author/", views.CreateAuthorView.as_view(), name="create_author"),
    path("manage-author/<int:pk>/", views.RetrieveUpdateDeleteAuthorView.as_view(), name="manage_author"),
    path("list-author/", views.ListAuthorView.as_view(), name="list_author"),
]
