from django.contrib import admin
from .models import Order, OrderItem, Bill


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "status", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "total", "created_at")