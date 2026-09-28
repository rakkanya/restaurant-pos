from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "ผู้ดูแลระบบ"
        STAFF = "staff", "พนักงาน"
        CUSTOMER = "customer", "ลูกค้า"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField("เบอร์โทร", max_length=20, blank=True)
    points = models.PositiveIntegerField("แต้มสมาชิก", default=0)

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_staff_user(self):
        return self.role in (self.Role.ADMIN, self.Role.STAFF) or self.is_superuser