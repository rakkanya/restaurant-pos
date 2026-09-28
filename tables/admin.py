from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats", "status")
    list_filter = ("status",)
    search_fields = ("number",)