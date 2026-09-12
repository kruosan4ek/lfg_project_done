"""
Формы для приложения LFG.
"""
from django import forms
from .models import LFGPost, Clan, Review


class LFGPostForm(forms.ModelForm):
    """Форма создания/редактирования LFG объявления."""
    class Meta:
        model = LFGPost
        fields = ['game', 'title', 'description', 'required_rank', 'required_roles', 'voice_chat_required']
        labels = {
            'game': 'Игра',
            'title': 'Заголовок',
            'description': 'Описание',
            'required_rank': 'Требуемый ранг',
            'required_roles': 'Требуемые роли',
            'voice_chat_required': 'Голосовой чат обязателен',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'required_roles': forms.CheckboxSelectMultiple(),
        }


class ClanForm(forms.ModelForm):
    """Форма создания клана."""
    class Meta:
        model = Clan
        fields = ['name', 'tag', 'game', 'description', 'logo']
        labels = {
            'name': 'Название клана',
            'tag': 'Тег клана',
            'game': 'Игра',
            'description': 'Описание',
            'logo': 'Эмблема',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    """Форма создания отзыва."""
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'is_toxic']
        labels = {
            'rating': 'Оценка (1-5)',
            'comment': 'Комментарий',
            'is_toxic': 'Токсичный игрок',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }