from django.urls import path

from reference_values import views

app_name = 'reference_values'

urlpatterns = [
    path('add-language/', views.CreateLanguageView.as_view(), name='add_language'),
    path('manage-language/<int:pk>', views.RetrieveUpdateDeleteLanguageView.as_view(), name='manage_language'),
    path('list-language/', views.ListLanguageView.as_view(), name='list_language'),
]
