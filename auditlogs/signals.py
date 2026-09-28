from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from menus.models import MenuItem
from tables.models import Table
from orders.models import Order
from .models import AuditLog

User = get_user_model()


def write_log(instance, action):
    AuditLog.objects.create(
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(getattr(instance, "pk", "")),
        detail=str(instance),
    )


@receiver(post_save, sender=MenuItem)
def log_menu_save(sender, instance, created, **kwargs):
    write_log(instance, "สร้าง" if created else "แก้ไข")


@receiver(post_delete, sender=MenuItem)
def log_menu_delete(sender, instance, **kwargs):
    write_log(instance, "ลบ")


@receiver(post_save, sender=Table)
def log_table_save(sender, instance, created, **kwargs):
    write_log(instance, "สร้าง" if created else "แก้ไข")


@receiver(post_save, sender=Order)
def log_order_save(sender, instance, created, **kwargs):
    write_log(instance, "สร้าง" if created else "แก้ไข")