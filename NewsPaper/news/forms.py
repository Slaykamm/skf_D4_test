from django.forms import ModelForm
from .models import Post
from django import forms
from django.forms import Select, TextInput, SelectMultiple, Textarea
 
 

# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['post_title', 'article_text', 'rating_article',  'position', 'author_post',]

