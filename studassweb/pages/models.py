from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from solo.models import SingletonModel
from base.fields import ValidatedRichTextField
from menu.models import MenuItem, Menu
from users.permissions import has_user_perm
from frontpage.models import FrontPageItem
import pages.register as pregister


PERMISSION_CHOICES = (
    (pregister.VIEW_PUBLIC, "Visible for everyone"),
    (pregister.VIEW_MEMBER, "Visible for members"),
    (pregister.VIEW_BOARD, "Visible for board members"),
)


class InfoCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)
    # an info category has an associated menu item, which in turn has a submenu
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)

    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES, default="VIEW_PUBLIC")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pages_view_category", kwargs={'slug': self.slug})

    def pages(self):
        return InfoPage.objects.filter(category=self)

    def can_view(self, user):
        return has_user_perm(user, self.permission)

    @staticmethod
    def can_edit(user):
        return has_user_perm(user, pregister.EDIT)

    def slugify(self, attempt=None):
        slug = slugify(self.name)
        if attempt is not None:
            slug += "-" + str(attempt)
        try:
            InfoCategory.objects.get(slug=slug)
            if attempt is None:
                attempt = 1
            else:
                attempt += 1
            return self.slugify(attempt)
        except InfoCategory.DoesNotExist:
            return slug


@receiver(pre_save, sender=InfoCategory, dispatch_uid="category_pre_save")
def category_pre_save(**kwargs):
    instance = kwargs.pop("instance")
    if not instance.pk:
        instance.slug = instance.slugify()


@receiver(post_save, sender=InfoCategory, dispatch_uid="category_post_save")
def category_post_save(**kwargs):
    instance = kwargs.pop("instance")
    # create a menu item if it doesn't exist
    instance.menu_item, created = MenuItem.get_or_create(identifier="pages/category/%d" % instance.id,
                                                         app_name=__package__,
                                                         display_name=instance.name,
                                                         linked_object=instance,
                                                         permission=instance.permission)
    if created:
        instance.menu_item.submenu, created2 = Menu.get_or_create(__package__ + "_category_" + instance.name)
        instance.menu_item.save()
        instance.save()


@receiver(pre_delete, sender=InfoCategory, dispatch_uid="category_pre_delete")
def category_pre_delete(**kwargs):
    instance = kwargs.pop("instance")
    instance.menu_item.delete()


class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    text = ValidatedRichTextField()
    category = models.ForeignKey(InfoCategory, null=True, blank=True)
    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES, default="VIEW_PUBLIC")
    for_frontpage = models.BooleanField(default=False,
                                        blank=True,
                                        help_text=_("Is this meant to be shown on the front page?"))
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages_view_page", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pk:
            # This is an update, so we want to save the old text
            old_page = InfoPage.objects.get(pk=self.pk)
        else:
            old_page = None
            # Create a slug for new pages
            self.slug = self.slugify()
        super(InfoPage, self).save(*args, **kwargs)

    def can_view(self, user):
        return has_user_perm(user, self.permission)

    @staticmethod
    def can_edit(user):
        return has_user_perm(user, pregister.EDIT)

    def revisions(self):
        return InfoPageEdit.objects.filter(page=self)

    def date(self):
        return self.revisions().first().date

    def update_frontpage_item(self):
        old = FrontPageItem.get_with_target(self)
        if self.for_frontpage:
            # create or update
            if old:
                old.title = self.title
                old.content = self.text
                old.identifier = self.slug
                old.save()
            else:
                new = FrontPageItem(title=self.title,
                                    content=self.text,
                                    identifier="pages/" + self.slug,
                                    location=FrontPageItem.HIDDEN
                                    )
                new.set_target(self)
                new.save()
        # remove if it exists
        elif old:
            old.delete()

    def slugify(self, attempt=None):
        slug = slugify(self.title)
        if attempt is not None:
            slug += "-" + str(attempt)
        try:
            InfoPage.objects.get(slug=slug)
            if attempt is None:
                attempt = 1
            else:
                attempt += 1
            return self.slugify(attempt)
        except InfoPage.DoesNotExist:
            return slug


@receiver(pre_delete, sender=InfoPage, dispatch_uid="page_pre_delete")
def page_pre_delete(**kwargs):
    instance = kwargs.pop("instance")
    print("calling InfoPage.pre_delete")
    MenuItem.delete_all_that_links_to(instance)


@receiver(post_delete, sender=InfoPage, dispatch_uid="page_post_delete")
def page_post_delete(**kwargs):
    instance = kwargs.pop("instance")
    # Remove any frontpage item associated to this one
    instance.for_frontpage = False
    instance.update_frontpage_item()


@receiver(post_save, sender=InfoPage, dispatch_uid="page_post_save")
def page_post_save(**kwargs):
    instance = kwargs.pop("instance")
    # create an edit object if this is a new object of if the text has changed
    if not instance.revisions().exists() or instance.revisions().first().text != instance.text\
            or instance.revisions().first().title != instance.title:
        edit = InfoPageEdit(author=instance.author,
                            title=instance.title,
                            text=instance.text,
                            page=instance)
        edit.save()
    # create a menu item if it doesn't exist
    menu_item, created = MenuItem.get_or_create(identifier="pages/page/%d" % instance.id,
                                                app_name=__package__,
                                                display_name=instance.title,
                                                linked_object=instance,
                                                permission=instance.permission)
    # Update the menu item
    if not created:
        menu_item.display_name = instance.title
        menu_item.permission = instance.permission
        menu_item.save()

    if instance.category:
        menu = instance.category.menu_item.submenu
        if not menu.contains(menu_item):
            # and add it last in the correct one
            menu.add_item(menu_item, menu.count())

    instance.update_frontpage_item()


class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    text = ValidatedRichTextField()
    date = models.DateTimeField('Date edited', auto_now_add=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return "%s - %s" % (self.page.title, self.date)

    def get_absolute_url(self):
        return reverse("pages_view_page", kwargs={'slug': self.page.slug,
                                                  'revision_id': self.id})

    def is_latest(self):
        return not InfoPageEdit.objects.filter(date__gt=self.date).exists()


class PagesSettings(SingletonModel):
    is_setup = models.BooleanField(default=False)

    @classmethod
    def instance(cls):
        instance, created = cls.objects.get_or_create()
        return instance