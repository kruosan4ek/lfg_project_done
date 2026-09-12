"""
Формы для приложения accounts.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {'username': 'Имя пользователя'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Bootstrap-классы
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
    """Форма редактирования профиля с Bootstrap-стилями."""

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'discord_tag', 'steam_id', 'bio']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'avatar': 'Аватар',
            'discord_tag': 'Discord',
            'steam_id': 'Steam ID',
            'bio': 'О себе',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'discord_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'steam_id': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }