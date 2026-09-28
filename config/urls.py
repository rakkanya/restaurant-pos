from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reports.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("", include("accounts.urls")),
    path("menus/", include("menus.urls")),
    path("tables/", include("tables.urls")),
    path("orders/", include("orders.urls")),
    path("reports/", include("reports.urls")),
    path("logs/", include("auditlogs.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)