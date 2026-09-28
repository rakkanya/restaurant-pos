import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
app = application

try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    call_command("migrate", interactive=False)
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="12345678",
        )
        admin = User.objects.get(username="admin")
        if hasattr(admin, "role"):
            admin.role = "admin"
            admin.save()
except Exception:
    pass