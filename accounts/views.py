"""
Представления для приложения accounts.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .utils import add_bootstrap_classes


def register_view(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации сразу входит в систему.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать в LFG!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    Просмотр профиля текущего пользователя.
    """
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    add_bootstrap_classes(form)
    return render(request, 'accounts/profile_edit.html', {'form': form})