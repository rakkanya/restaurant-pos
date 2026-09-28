from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Category, MenuItem


@login_required
def menu_list(request):
    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    items = MenuItem.objects.select_related("category").all()
    if q:
        items = items.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    if category_id:
        items = items.filter(category_id=category_id)
    page = Paginator(items.order_by("name"), 10).get_page(request.GET.get("page"))
    categories = Category.objects.filter(is_active=True)
    return render(request, "menus/menu_list.html", {
        "page": page,
        "q": q,
        "category_id": category_id,
        "categories": categories,
    })