from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.StaffLoginView.as_view(), name="login"),
    path("logout/", views.StaffLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/edit/", views.user_edit, name="user_edit"),
]