from django.contrib import admin
from .models import Article, ArticleInCategory, Category

admin.site.register(Article)
admin.site.register(ArticleInCategory)
admin.site.register(Category)