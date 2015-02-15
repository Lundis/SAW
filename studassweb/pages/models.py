from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from base.fields import ValidatedRichTextField
from menu.models import MenuItem, Menu
from users.permissions import has_user_perm
from frontpage.models import FrontPageItem
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete
import pages.register as pregister

PERMISSION_CHOICES = (
    ("VIEW_PUBLIC", pregister.VIEW_PUBLIC),
    ("VIEW_MEMBER", pregister.VIEW_MEMBER),
    ("VIEW_BOARD", pregister.VIEW_BOARD),
)


class InfoCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(editable=False)
    # an info category has an associated menu item, which in turn has a submenu
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)

    permission = models.CharField(max_length=15, choices=PERMISSION_CHOICES, default="VIEW_PUBLIC")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pages_view_category", kwargs={'slug': self.slug})

    def pages(self):
        return InfoPage.objects.filter(category=self)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(InfoCategory, self).save(*args, **kwargs)
        # create a menu item if it doesn't exist
        self.menu_item, created = MenuItem.get_or_create(identifier="pages/category/%d" % self.id,
                                                         app_name=__package__,
                                                         display_name=self.name,
                                                         linked_object=self,
                                                         permission=self.permission)
        if created:
            self.menu_item.submenu, created2 = Menu.get_or_create(__package__ + "_category_" + self.name)
            self.menu_item.save()
            self.save()
            info_menu, created = Menu.get_or_create("pages_top_menu")
            info_menu.add_item(self.menu_item)

    def can_view(self, user):
        return has_user_perm(user, self.get_permission_str())

    @staticmethod
    def can_edit(user):
        return has_user_perm(user, pregister.EDIT)

    def get_permission_str(self):
        return dict(PERMISSION_CHOICES)[self.permission]


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
            self.slug = slugify(self.title)
        super(InfoPage, self).save(*args, **kwargs)
        # create an edit object if this is a new object of if the text has changed
        if not old_page or old_page.text != self.text:
            edit = InfoPageEdit(author=self.author, text=self.text, page=self)
            edit.save()
        # create a menu item if it doesn't exist
        menu_item, created = MenuItem.get_or_create(identifier="pages/page/%d" % self.id,
                                                    app_name=__package__,
                                                    display_name=self.title,
                                                    linked_object=self,
                                                    permission=self.permission)
        if self.category:
            menu = self.category.menu_item.submenu
            if not menu.contains(menu_item):
                # delete it from any other menus
                Menu.remove_item_from_all_menus(menu_item)
                # and add it last in the correct one
                menu.add_item(menu_item, menu.count())

        self.update_frontpage_item()

    def can_view(self, user):
        return has_user_perm(user, self.get_permission_str())

    @staticmethod
    def can_edit(user):
        return has_user_perm(user, pregister.EDIT)

    def get_permission_str(self):
        return dict(PERMISSION_CHOICES)[self.permission]

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


@receiver(pre_delete, sender=InfoPage, dispatch_uid="page_pre_delete")
def page_pre_delete(**kwargs):
    instance = kwargs.pop("instance")
    print("calling InfoPage.pre_delete")
    MenuItem.delete_all_that_links_to(instance)


@receiver(pre_delete, sender=InfoPage, dispatch_uid="page_post_delete")
def page_post_delete(**kwargs):
    instance = kwargs.pop("instance")
    instance.update_frontpage_item()


class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
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