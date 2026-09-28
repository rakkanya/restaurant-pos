from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard_page"),
    path("sales/", views.sales_report, name="sales_report"),
]