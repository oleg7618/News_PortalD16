"""
Данный файл нужен для создания форм на страницах приложения
Пользователь сможет взаимодействовать с объектами, например добавлять их,
через страницы приложения.
"""
from django.forms import ModelForm
from .models import Post



# Создаём модельную форму
class PostForm(ModelForm):
    # В класс мета,
    # Что-то похожее нужно делать с фильтрами с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'view', 'post_category']

