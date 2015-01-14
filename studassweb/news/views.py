from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from users.decorators import has_permission
from .models import Article, Category
from .forms import ArticleForm, CategoryForm
from .register import EDIT
import datetime

ARTICLES_PER_PAGE = 10


def home(request, page=0, category_id=None):
    page = int(page)
    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass
        articles = Article.objects.filter(categories__id=category_id)
    else:
        articles = Article.objects.all()
        category = None

    articles = articles[page*ARTICLES_PER_PAGE:(page + 1)*ARTICLES_PER_PAGE]
    categories = Category.objects.all()
    context = {'articles': articles,
               'categories': categories,
               'category': category}
    return render(request, "news/view_news.html", context)


def view_article(request, year, month, day, slug):
    date = datetime.date(year=int(year), month=int(month), day=int(day))
    try:
        article = Article.objects.get(created_date=date, slug=slug)
    except Article.DoesNotExist:
        raise Http404(_("The requested article could not be found!"))
    context = {'article': article}
    return render(request, "news/view_article.html", context)


@has_permission(EDIT)
def edit_article(request, slug=None):
    if slug is not None:
        try:
            member = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404(_("The requested article could not be found!"))
    else:
        member = None
    form = ArticleForm(request.POST or None,
                       request.FILES or None,
                       instance=member)
    if form.is_valid():
        article = form.save(user=request.user)
        return HttpResponseRedirect(article.get_absolute_url())
    else:
        context = {'member': member,
                   'form': form}
        return render(request, 'news/add_edit_article.html', context)


@has_permission(EDIT)
def delete_article(request):
    pass


@has_permission(EDIT)
def edit_category(request, category_id=None):
    if category_id is not None:
        try:
            category = Article.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404(_("Category does not exist"))
    else:
        category = None
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("news_home"))
    else:
        context = {'category': category,
                   'form': form}
        return render(request, 'news/edit_category.html', context)