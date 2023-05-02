from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):    
    password_confirmation = forms.CharField(
        label='Подтверждение пароля:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'input_type': 'password'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'password')
        labels = {
            'first_name': 'Имя:',
            'last_name': 'Фамилия:',
            'middle_name': 'Отчество (необязательно):',
            'phone_number': 'Номер телефона (+7-xxx-xxx-xx-xx)',
            'password': 'Пароль:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'input_type': 'tel'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'input_type': 'password'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages['required'] = 'Это поле обязательное'
        
        self.fields['phone_number'].error_messages['unique'] = 'Номер телефона уже существует.'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number').strip().replace('-', '')

        if not phone_number.startswith('+7'):
            raise forms.ValidationError("Номер телефона должен начинаться с +7")
        
        if not phone_number[2:].isdigit() or len(phone_number[2:]) != 10:
            raise forms.ValidationError("Номер телефона должен содержать 10 цифр после кода страны")
        
        return phone_number
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов и хотя бы одну цифру.")
        
        return password

    def clean_password_confirmation(self):
        password_confirmation = self.cleaned_data.get("password_confirmation")
        password = self.cleaned_data.get("password")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Пароли не совпадают")
        
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
    phone_number = forms.CharField(
        label='Номер телефона:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'input_type': 'tel', 'required': True})
    )

    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'input_type': 'password'})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number').strip().replace('-', '')

        if not phone_number.startswith('+7'):
            raise forms.ValidationError("Номер телефона должен начинаться с +7")
        
        if not phone_number[2:].isdigit() or len(phone_number[2:]) != 10:
            raise forms.ValidationError("Номер телефона должен содержать 10 цифр после кода страны")
        
        return phone_number
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов и хотя бы одну цифру.")
        
        return password