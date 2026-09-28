from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from menus.models import MenuItem
from tables.models import Table
from .models import Bill, Order, OrderItem


def staff_only(user):
    return user.is_authenticated and (
        getattr(user, "role", "") in ("admin", "staff") or user.is_superuser
    )


@login_required
def kitchen(request):
    if not staff_only(request.user):
        return HttpResponseForbidden("หน้านี้สำหรับพนักงานเท่านั้น")
    orders = (
        Order.objects.exclude(status__in=["paid", "cancelled"])
        .prefetch_related("items", "items__menu_item")
        .order_by("created_at")
    )
    return render(request, "orders/kitchen.html", {"orders": orders})


@login_required
def checkout(request, order_id):
    if not staff_only(request.user):
        return HttpResponseForbidden("หน้านี้สำหรับพนักงานเท่านั้น")
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    subtotal = sum((item.unit_price * item.quantity) for item in items)

    if request.method == "POST":
        raw = request.POST.get("discount", "0")
        try:
            discount = Decimal(raw)
        except Exception:
            discount = Decimal("0")
        if discount < 0:
            discount = Decimal("0")
        service = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
        tax = (subtotal * Decimal("0.07")).quantize(Decimal("0.01"))
        total = subtotal + service + tax - discount
        if total < 0:
            total = Decimal("0.00")
        bill, _ = Bill.objects.get_or_create(order=order)
        bill.subtotal = subtotal
        bill.service_charge = service
        bill.tax = tax
        bill.discount = discount
        bill.total = total
        bill.save()
        order.status = Order.Status.PAID
        order.save()
        order.table.status = Table.Status.EMPTY
        order.table.save()
        return redirect("receipt", order_id=order.id)

    service = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
    tax = (subtotal * Decimal("0.07")).quantize(Decimal("0.01"))
    return render(request, "orders/checkout.html", {
        "order": order,
        "items": items,
        "subtotal": subtotal,
        "service": service,
        "tax": tax,
        "total": subtotal + service + tax,
    })


@login_required
def receipt(request, order_id):
    if not staff_only(request.user):
        return HttpResponseForbidden("หน้านี้สำหรับพนักงานเท่านั้น")
    order = get_object_or_404(Order, id=order_id)
    bill = get_object_or_404(Bill, order=order)
    return render(request, "orders/receipt.html", {"order": order, "bill": bill})


def table_order(request, table_no):
    table = get_object_or_404(Table, number=table_no)
    menus = MenuItem.objects.filter(is_active=True).select_related("category")
    message = ""
    order = Order.objects.filter(table=table, status=Order.Status.OPEN).first()

    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        qty_raw = request.POST.get("qty", "1")
        action = request.POST.get("action", "add")
        try:
            qty = int(qty_raw)
        except (TypeError, ValueError):
            qty = 0
        item = MenuItem.objects.filter(id=menu_id).first()

        if item is None:
            message = "ไม่พบเมนู"
        elif item.status == MenuItem.Status.SOLD_OUT:
            message = "เมนูนี้หมดแล้ว"
        elif qty < 1:
            message = "จำนวนต้องมากกว่า 0"
        else:
            if order is None:
                order = Order.objects.create(table=table, status=Order.Status.OPEN)
                table.status = Table.Status.OCCUPIED
                table.save()
            line = order.items.filter(menu_item=item).first()
            if action == "cancel" and line:
                line.status = OrderItem.Status.CANCELLED
                line.save()
                message = "ยกเลิกรายการแล้ว"
            elif line:
                line.quantity += qty
                line.save()
                message = "เพิ่มจำนวนแล้ว"
            else:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    unit_price=item.price,
                )
                message = "เพิ่มออเดอร์แล้ว"

    if order:
        order = Order.objects.prefetch_related("items", "items__menu_item").get(id=order.id)

    return render(request, "orders/table_order.html", {
        "table": table,
        "menus": menus,
        "order": order,
        "message": message,
    })