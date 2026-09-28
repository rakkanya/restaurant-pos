from django.conf import settings
from django.db import models
from menus.models import MenuItem
from tables.models import Table


class Order(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "เปิดอยู่"
        COOKING = "cooking", "กำลังทำ"
        SERVED = "served", "เสิร์ฟแล้ว"
        PAID = "paid", "ชำระแล้ว"
        CANCELLED = "cancelled", "ยกเลิก"

    table = models.ForeignKey(Table, on_delete=models.PROTECT, verbose_name="โต๊ะ")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField("สถานะ", max_length=20, choices=Status.choices, default=Status.OPEN)
    note = models.CharField("หมายเหตุ", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ออเดอร์"
        verbose_name_plural = "ออเดอร์"
        ordering = ["-created_at"]

    def __str__(self):
        return f"ออเดอร์โต๊ะ {self.table.number}"


class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "รอดำเนินการ"
        COOKING = "cooking", "กำลังทำ"
        DONE = "done", "เสร็จ"
        CANCELLED = "cancelled", "ยกเลิก"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, verbose_name="เมนู")
    quantity = models.PositiveIntegerField("จำนวน", default=1)
    unit_price = models.DecimalField("ราคาต่อหน่วย", max_digits=10, decimal_places=2)
    status = models.CharField("สถานะ", max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        verbose_name = "รายการอาหาร"
        verbose_name_plural = "รายการอาหาร"

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"


class Bill(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, verbose_name="ออเดอร์")
    subtotal = models.DecimalField("ยอดก่อนคิด", max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField("ค่าบริการ", max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField("ภาษี", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField("ส่วนลด", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField("ยอดสุทธิ", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "บิล"
        verbose_name_plural = "บิล"

    def __str__(self):
        return f"บิล {self.order}"