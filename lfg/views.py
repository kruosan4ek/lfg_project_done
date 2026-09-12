"""
Представления для приложения LFG.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LFGPost, Clan, Game, ClanMembership
from .forms import LFGPostForm, ClanForm

def home_view(request):
    """
    Главная страница со списком активных объявлений.
    """
    posts = LFGPost.objects.filter(status='open').order_by('-created_at')
    games = Game.objects.filter(is_active=True)
    return render(request, 'lfg/home.html', {
        'posts': posts,
        'games': games,
    })


@login_required
def lfg_create_view(request):
    """
    Создание нового LFG объявления.
    """
    if request.method == 'POST':
        form = LFGPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Объявление создано!')
            return redirect('lfg_detail', pk=post.pk)
    else:
        form = LFGPostForm()
    return render(request, 'lfg/lfg_form.html', {'form': form, 'action': 'Создать'})


def lfg_detail_view(request, pk):
    """
    Детальный просмотр LFG объявления.
    """
    post = get_object_or_404(LFGPost, pk=pk)
    return render(request, 'lfg/lfg_detail.html', {'post': post})


@login_required
def lfg_update_view(request, pk):
    """
    Редактирование LFG объявления (только автор).
    """
    post = get_object_or_404(LFGPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = LFGPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено!')
            return redirect('lfg_detail', pk=post.pk)
    else:
        form = LFGPostForm(instance=post)
    return render(request, 'lfg/lfg_form.html', {'form': form, 'action': 'Редактировать'})


@login_required
def lfg_delete_view(request, pk):
    """
    Удаление LFG объявления (только автор).
    """
    post = get_object_or_404(LFGPost, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Объявление удалено!')
        return redirect('home')
    return render(request, 'lfg/lfg_confirm_delete.html', {'post': post})


def clan_list_view(request):
    """
    Список всех кланов.
    """
    clans = Clan.objects.all().order_by('-created_at')
    return render(request, 'lfg/clan_list.html', {'clans': clans})


def clan_detail_view(request, pk):
    """
    Детальная страница клана.
    """
    clan = get_object_or_404(Clan, pk=pk)
    members = ClanMembership.objects.filter(clan=clan).select_related('user')
    return render(request, 'lfg/clan_detail.html', {'clan': clan, 'memberships': members})


@login_required
def clan_create_view(request):
    """
    Создание нового клана.
    """
    if request.method == 'POST':
        form = ClanForm(request.POST, request.FILES)
        if form.is_valid():
            clan = form.save(commit=False)
            clan.leader = request.user
            clan.save()
            ClanMembership.objects.create(clan=clan, user=request.user, role='leader')
            messages.success(request, 'Клан создан!')
            return redirect('clan_detail', pk=clan.pk)
    else:
        form = ClanForm()
    return render(request, 'lfg/clan_form.html', {'form': form})


def add_to_favorites(request, post_id):
    """
    Добавление объявления в избранное через сессию.
    """
    favorites = request.session.get('favorites', [])
    if post_id not in favorites:
        favorites.append(post_id)
        request.session['favorites'] = favorites
        messages.success(request, 'Добавлено в избранное!')
    return redirect('home')


def favorites_view(request):
    """
    Просмотр избранных объявлений из сессии.
    """
    favorites = request.session.get('favorites', [])
    posts = LFGPost.objects.filter(id__in=favorites)
    return render(request, 'lfg/favorites.html', {'posts': posts})

def chat_room_view(request, pk):
    """Страница чата для LFG объявления."""
    post = get_object_or_404(LFGPost, pk=pk)
    return render(request, 'lfg/chat_room.html', {'post': post})