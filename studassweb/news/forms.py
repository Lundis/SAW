# coding=utf-8
from django import forms
from .models import Article
from .models import Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "text", "picture", "categories", "summary"]

    def save(self, commit=True, user=None):
        article = super().save(commit=False)
        if not hasattr(article, "author") and user is not None:
            article.author = user
        if commit:
            article.save()
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            # So we need this method because we used commit=False earlier
            self.save_m2m()
        return article


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
