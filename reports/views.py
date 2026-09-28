from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render
from django.utils import timezone
from orders.models import Bill, OrderItem


@login_required
def dashboard(request):
    return render(request, "reports/dashboard.html")


@login_required
def sales_report(request):
    today = timezone.localdate()
    bills = Bill.objects.filter(created_at__date=today)
    total_sales = bills.aggregate(s=Sum("total"))["s"] or 0
    bill_count = bills.count()
    top_menus = (
        OrderItem.objects.filter(order__bill__created_at__date=today)
        .values("menu_item__name")
        .annotate(qty=Sum("quantity"), sales=Sum(F("unit_price") * F("quantity")))
        .order_by("-qty")[:10]
    )
    return render(request, "reports/sales.html", {
        "today": today,
        "total_sales": total_sales,
        "bill_count": bill_count,
        "top_menus": top_menus,
    })