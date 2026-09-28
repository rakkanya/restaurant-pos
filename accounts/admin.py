from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active")
    fieldsets = UserAdmin.fieldsets + (("บทบาท", {"fields": ("role", "phone", "points")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("บทบาท", {"fields": ("role", "phone")}),)