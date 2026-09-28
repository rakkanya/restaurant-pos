from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="ชื่อ", max_length=150)
    last_name = forms.CharField(label="นามสกุล", max_length=150, required=False)
    email = forms.EmailField(label="อีเมล")
    phone = forms.CharField(label="เบอร์โทร", max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if len(username) < 4:
            raise forms.ValidationError("ชื่อผู้ใช้ต้องมีอย่างน้อย 4 ตัวอักษร")
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="ชื่อผู้ใช้")
    password = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput)


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "role", "is_active")