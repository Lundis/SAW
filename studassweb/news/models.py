from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from base.models import Comment
from base.fields import ValidatedRichTextField


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
    # split the date and time in order to make fetching articles based on date easier
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # A small thumbnail used in the news feed
    picture = models.ImageField(upload_to="news/article_thumbnails", blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
