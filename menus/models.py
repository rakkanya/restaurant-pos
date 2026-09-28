from django.db import models


class Category(models.Model):
    name = models.CharField("หมวดหมู่", max_length=100)
    is_active = models.BooleanField("ใช้งาน", default=True)

    class Meta:
        verbose_name = "หมวดหมู่"
        verbose_name_plural = "หมวดหมู่"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "พร้อมขาย"
        SOLD_OUT = "sold_out", "หมด"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="หมวดหมู่")
    name = models.CharField("ชื่อเมนู", max_length=150)
    price = models.DecimalField("ราคา", max_digits=10, decimal_places=2)
    image = models.ImageField("รูปภาพ", upload_to="menu_images/", blank=True, null=True)
    status = models.CharField("สถานะ", max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    is_active = models.BooleanField("แสดงเมนู", default=True)

    class Meta:
        verbose_name = "เมนู"
        verbose_name_plural = "เมนู"

    def __str__(self):
        return self.name