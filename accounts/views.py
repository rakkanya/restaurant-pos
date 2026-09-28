from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RegisterForm, LoginForm, UserRoleForm
from .models import User


class StaffLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class StaffLogoutView(LogoutView):
    next_page = "login"


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = User.Role.CUSTOMER
        user.save()
        login(request, user)
        messages.success(request, "สมัครสมาชิกสำเร็จ")
        return redirect("dashboard")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def user_list(request):
    if not request.user.is_admin():
        messages.error(request, "เฉพาะผู้ดูแลระบบเท่านั้น")
        return redirect("dashboard")
    q = request.GET.get("q", "")
    role = request.GET.get("role", "")
    users = User.objects.all()
    if q:
        users = users.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(email__icontains=q)
        )
    if role:
        users = users.filter(role=role)
    page = Paginator(users, 10).get_page(request.GET.get("page"))
    return render(request, "accounts/user_list.html", {"page": page, "q": q, "role": role})


@login_required
def user_edit(request, pk):
    if not request.user.is_admin():
        return redirect("dashboard")
    user = get_object_or_404(User, pk=pk)
    form = UserRoleForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "บันทึกผู้ใช้แล้ว")
        return redirect("user_list")
    return render(request, "accounts/user_form.html", {"form": form, "obj": user})