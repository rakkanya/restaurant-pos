from django.db import models


class Table(models.Model):
    class Status(models.TextChoices):
        EMPTY = "empty", "ว่าง"
        OCCUPIED = "occupied", "มีลูกค้า"
        BILLING = "billing", "รอเช็คบิล"

    number = models.PositiveIntegerField("หมายเลขโต๊ะ", unique=True)
    seats = models.PositiveIntegerField("จำนวนที่นั่ง", default=4)
    status = models.CharField("สถานะ", max_length=20, choices=Status.choices, default=Status.EMPTY)

    class Meta:
        verbose_name = "โต๊ะ"
        verbose_name_plural = "โต๊ะ"
        ordering = ["number"]

    def __str__(self):
        return f"โต๊ะ {self.number}"