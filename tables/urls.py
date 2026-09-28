from django.urls import path
from . import views

urlpatterns = [
    path("qr/", views.qr_list, name="qr_list"),
]