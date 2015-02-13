from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FrontPageItem(models.Model):
    identifier = models.CharField(max_length=100)
    title = models.TextField()
    content = models.TextField()

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

    def save(self, *args, **kwargs):
        """
        Try
        :param args:
        :param kwargs:
        :return:
        """
        if not self.pk:
            # Put it last
            self.ordering_index = self._count_in_location() + 1
        else:
            try:
                # Get the object currently at the wanted position:
                other = FrontPageItem.objects.get(location=self.location,
                                                  ordering_index=self.ordering_index)
                # and move it forward
                if self.pk != other.pk:
                    other.ordering_index += 1
                    other.save()
            except FrontPageItem.DoesNotExist:
                pass

        super(FrontPageItem, self).save(*args, **kwargs)
        self._fix_indices()

    def delete(self, using=None):
        super(FrontPageItem, self).delete(using)
        # Remove any inconsistencies caused by this deletion
        self._fix_indices()

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

    @classmethod
    def get_with_target(cls, target):
        try:
            return cls.objects.get(_content_type=ContentType.objects.get_for_model(target),
                                   _object_id=target.id)
        except cls.DoesNotExist:
            return None