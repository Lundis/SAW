from django import forms
from .models import Article
from .models import Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "text", "picture", "categories", "summary"]

    def save(self, commit=True, user=None):
        article = super(ArticleForm, self).save(commit=False)
        if not hasattr(article, "author") and user is not None:
            article.author = user
        if commit:
            article.save()
        return article


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]