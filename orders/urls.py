from django.urls import path
from . import views

urlpatterns = [
    path("kitchen/", views.kitchen, name="kitchen"),
    path("checkout/<int:order_id>/", views.checkout, name="checkout"),
    path("receipt/<int:order_id>/", views.receipt, name="receipt"),
    path("table/<int:table_no>/", views.table_order, name="table_order"),
]