from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Table


@login_required
def qr_list(request):
    tables = Table.objects.all().order_by("number")
    return render(request, "orders/qr.html", {"tables": tables})