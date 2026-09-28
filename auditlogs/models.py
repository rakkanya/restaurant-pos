from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField("การกระทำ", max_length=50)
    model_name = models.CharField("ตาราง", max_length=100)
    object_id = models.CharField("รหัสข้อมูล", max_length=50, blank=True)
    detail = models.TextField("รายละเอียด", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} {self.model_name}"