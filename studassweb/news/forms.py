from django import forms
from .models import Article
from .models import Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "summary", "text", "picture", "categories"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]