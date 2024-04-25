from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)  # 手机号为选填

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone_number")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # 由于 post_save 信号会创建 Profile，此处确保数据库提交完成后修改 Profile
            user.refresh_from_db()  # 刷新用户实例以确保 Profile 已创建
            if self.cleaned_data["phone_number"]:
                user.profile.phone_number = self.cleaned_data["phone_number"]
                user.profile.save()
        return user
class MassageLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    
