from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreationForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'password')

    def clean_password_confirmation(self):
        password_confirmation = self.cleaned_data.get("password_confirmation")
        password = self.cleaned_data.get("password")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.cleaned_data:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'phone_number', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)