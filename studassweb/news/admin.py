from django.contrib import admin
from .models import Article, ArticleInCategory, Category


class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ClientAdmin)
admin.site.register(ArticleInCategory)
admin.site.register(Category)