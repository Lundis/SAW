from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from solo.models import SingletonModel
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save

from base.models import Comment
from base.fields import ValidatedRichTextField
from base.html_stripper import strip_html


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("news_home", kwargs={'category_name': self.name})

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=300, blank=True, null=True)
    slug = models.SlugField(editable=False)
    text = ValidatedRichTextField()
    search_text = models.TextField(editable=False, blank=True)
    # split the date and time in order to make fetching articles based on date easier
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # A small thumbnail used in the news feed
    picture = models.ImageField(upload_to="news/article_thumbnails", blank=True, null=True,
                                help_text="A small picture used in the news feed")
    author = models.ForeignKey(User)
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ["-created_date", "-created_time"]
        unique_together = ("slug", "created_date")

    def get_summary(self):
        if self.summary:
            return self.summary
        else:
            if len(self.text) > 300:
                summary = ValidatedRichTextField.get_summary(self.text, 300)
                return "%s<p><strong>...</strong></p>" % summary
            else:
                return self.text

    def comments(self):
        """
        :return: A QuerySet of the comments for this object
        """
        return Comment.get_comments_for_object(self)

    def get_absolute_url(self):
        return reverse("news_view_article", kwargs={'slug': self.slug,
                                                    'year': self.created_date.year,
                                                    'month': self.created_date.month,
                                                    'day': self.created_date.day})

    def __str__(self):
        return self.title

    def update_frontpage_items(self):
        """
        Makes sure the N latest items exist as frontpage items
        :return:
        """
        # TODO Make sure the N latest items exist as frontpage items
        pass


@receiver(pre_save, sender=Article, dispatch_uid="article_pre_save")
def article_pre_save(**kwargs):
    instance = kwargs.pop("instance")
    # create slug at creation
    if not instance.pk:
        instance.slug = slugify(instance.title)
    # create search text
    instance.search_text = strip_html(instance.text).replace('\n', '').replace('\r', '')


@receiver(post_save, sender=Article, dispatch_uid="article_post_save")
def article_post_save(**kwargs):
    instance = kwargs.pop("instance")
    instance.update_frontpage_items()


@receiver(post_delete, sender=Article, dispatch_uid="article_post_delete")
def article_pre_delete(**kwargs):
    instance = kwargs.pop("instance")
    instance.update_frontpage_items()


class NewsSettings(SingletonModel):
    is_setup = models.BooleanField(default=False)

    @classmethod
    def instance(cls):
        self, created = cls.objects.get_or_create()
        return self
