from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, post_save, pre_save
from base.utils import get_function_from_module
import logging

logger = logging.getLogger(__name__)


class FrontPageItem(models.Model):
    """
    Represents a frontpage item. Choose between static content or a custom rendering function that
    is called every time.
    """
    identifier = models.CharField(max_length=100)
    title = models.TextField()
    content = models.TextField(null=True, blank=True)
    # TODO: figure out if template can be removed
    template = models.CharField(max_length=200, default="")
    # Which module this belongs to
    module = models.CharField(max_length=50, blank=True, default="")
    # an optional content rendering function (def func(front_page_item)),
    # which resides in module.frontpage
    render_function = models.CharField(max_length=50, blank=True, default="")


    MAINBAR = "MB"
    SIDEBAR = "SB"
    HIDDEN = "HD"

    LOCATION_CHOICES = (
        (MAINBAR, "Main bar"),
        (SIDEBAR, "Side bar"),
        (HIDDEN, "Hidden")
    )

    location = models.CharField(max_length=2, choices=LOCATION_CHOICES, default=HIDDEN)
    ordering_index = models.IntegerField(validators=[MinValueValidator(1)])

    # These are used if the item corresponds to a specific model, such as a news article
    _content_type = models.ForeignKey(ContentType, null=True, blank=True)
    _object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('_content_type', '_object_id')

    class Meta:
        unique_together = (("location", "ordering_index"),
                           ("_content_type", "_object_id"))
        ordering = "ordering_index",

    def __str__(self):
        return self.identifier

    def _fix_indices(self):
        pages = FrontPageItem.objects.filter(location=self.location)
        i = 1
        for page in pages:
            if page.ordering_index != i:
                page.ordering_index = 1
                page.save()
            i += 1

    def _count_in_location(self):
        return FrontPageItem.objects.filter(location=self.location).count()

    def set_target(self, target):
        """
        :param target: A Django Model
        :return:
        """
        self._content_type = ContentType.objects.get_for_model(target)
        self._object_id = target.id

    def render_content(self):
        """
        Renders the menu items using provided templates
        :return:
        """
        if self.module and self.render_function:
            render_func = get_function_from_module(self.module, "frontpage",
                                                   self.render_function)
            render_func(self)
        else:
            return self.content

    @classmethod
    def get_with_target(cls, target):
        try:
            return cls.objects.get(_content_type=ContentType.objects.get_for_model(target),
                                   _object_id=target.id)
        except cls.DoesNotExist:
            return None


@receiver(pre_save, sender=FrontPageItem, dispatch_uid="frontpage_item_pre_save")
def frontpage_item_pre_save(**kwargs):
    instance = kwargs.pop("instance")
    if not instance.ordering_index:
        # just try to place it first
        instance.ordering_index = 1

    try:
        logger.debug("Trying to save frontpage item at index %s" % instance.ordering_index)
        # Get the object currently at the wanted position:
        other = FrontPageItem.objects.get(location=instance.location,
                                          ordering_index=instance.ordering_index)
        # and move it forward
        if instance.pk != other.pk:
            logger.debug("Moving other frontpage item forward to position %s, saving self at %s" %
                         (other.ordering_index+1, other.ordering_index))
            other.ordering_index += 1
            other.save()
    except FrontPageItem.DoesNotExist:
        pass


@receiver(post_save, sender=FrontPageItem, dispatch_uid="frontpage_item_post_save")
def frontpage_item_post_save(**kwargs):
    instance = kwargs.pop("instance")