from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from users.decorators import has_permission
from .models import Article, Category
from .forms import ArticleForm, CategoryForm
from .register import EDIT
from base.views import delete_confirmation_view
import datetime
import logging

logger = logging.getLogger(__name__)

ARTICLES_PER_PAGE = 10


def home(request, page=1, category_name=None):
    context = {}
    category = None
    if not isinstance(page, int):
        try:
            page = int(page)
        except TypeError:
            page = 1

    if category_name is not None:
        try:
            category = Category.objects.get(name=category_name)
            articles = category.article_set.all()
        except Category.DoesNotExist:
            raise Http404(_("The category does not exist!"))
    if category is None:
        articles = Article.objects.all()
    else:
        context['category'] = category
    if request.GET.get('year', None) is not None:
        try:
            year = int(request.GET['year'])
            articles = articles.filter(created_date__year=year)
        except ValueError:
            pass
    if request.GET.get('month', None) is not None:
        try:
            month = int(request.GET['month'])
            articles = articles.filter(created_date__month=month)
        except ValueError:
            pass
    if request.GET.get('day', None) is not None:
        try:
            day = int(request.GET['day'])
            articles = articles.filter(created_date__day=day)
        except ValueError:
            pass
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    current_page = paginator.page(page)
    categories = Category.objects.all()
    context['articles'] = current_page.object_list
    context['categories'] = categories
    context['page'] = current_page
    context['paginator'] = paginator
    return render(request, "news/view_news.html", context)


def view_article(request, year, month, day, slug):
    date = datetime.date(year=int(year), month=int(month), day=int(day))
    try:
        article = Article.objects.get(created_date=date, slug=slug)
    except Article.DoesNotExist:
        raise Http404(_("The requested article could not be found!"))
    context = {'article': article,
               'categories': Category.objects.all()}
    return render(request, "news/view_article.html", context)


@has_permission(EDIT)
def edit_article(request, article_id=None):
    if article_id is not None:
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise Http404(_("The requested article could not be found!"))
    else:
        article = None
    form = ArticleForm(request.POST or None,
                       request.FILES or None,
                       instance=article)
    if form.is_valid():
        article = form.save(user=request.user)
        return HttpResponseRedirect(article.get_absolute_url())
    else:
        context = {'article': article,
                   'form': form}
        return render(request, 'news/add_edit_article.html', context)


@has_permission(EDIT)
def delete_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404(_("The requested article could not be found!"))
    return delete_confirmation_view(request,
                                    item=article,
                                    form_url=reverse("news_delete_article", args=(article_id,)),
                                    redirect_url=reverse("news_home"))


@has_permission(EDIT)
def edit_category(request, category_id=None):
    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404(_("The requested category does not exist"))
    else:
        category = None
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("news_home"))
    else:
        context = {'category': category,
                   'form': form}
        return render(request, 'news/add_edit_category.html', context)


@has_permission(EDIT)
def delete_category(request, category_id):
    try:
        article = Category.objects.get(id=category_id)
    except Article.DoesNotExist:
        raise Http404(_("The requested article could not be found!"))
    return delete_confirmation_view(request,
                                    item=article,
                                    form_url=reverse("news_delete_category", args=(category_id,)),
                                    redirect_url=reverse("news_home"))