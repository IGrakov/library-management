from django.urls import path, re_path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    re_path(
        r'^manage(?:/(?P<pk>\d+))?/$',
        views.ManageUserView.as_view(),
        name='manage',
    ),
    path('list/', views.ListUserView.as_view(), name='list'),
]
