from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)  # Mobile phone number is optional

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone_number")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Since the post_save signal creates a Profile, make sure that you modify the Profile after the database has been committed.
            user.refresh_from_db()  # Refresh the user instance to ensure that the Profile has been created
            if self.cleaned_data["phone_number"]:
                user.profile.phone_number = self.cleaned_data["phone_number"]
                user.profile.save()
        return user
class MassageLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16, min_length=16, widget=forms.NumberInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_expiry = forms.CharField(label='Expiry Date', max_length=5, min_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvc = forms.CharField(label='CVC', max_length=3, min_length=3, widget=forms.NumberInput(attrs={'placeholder': 'CVC'}))

    
