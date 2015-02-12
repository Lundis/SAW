from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from users.permissions import has_user_perm
from .register import CAN_VIEW_PUBLIC_POLLS, CAN_VIEW_MEMBER_POLLS, \
    CAN_VIEW_BOARD_POLLS, CAN_VOTE_PUBLIC_POLLS, CAN_VOTE_MEMBER_POLLS, CAN_VOTE_BOARD_POLLS
# Create your models here.

PERMISSION_CHOICES = (
    ("CAN_VIEW_PUBLIC_POLLS", CAN_VIEW_PUBLIC_POLLS),
    ("CAN_VIEW_MEMBER_POLLS", CAN_VIEW_MEMBER_POLLS),
    ("CAN_VIEW_BOARD_POLLS", CAN_VIEW_BOARD_POLLS),
    ("CAN_VOTE_PUBLIC_POLLS", CAN_VOTE_PUBLIC_POLLS),
    ("CAN_VOTE_MEMBER_POLLS", CAN_VOTE_MEMBER_POLLS),
    ("CAN_VOTE_BOARD_POLLS", CAN_VOTE_BOARD_POLLS),

)


class Poll(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    publication = models.DateTimeField('Date published')
    expiration = models.DateTimeField('Poll closes')
    created_by = models.ForeignKey(User)
    can_vote_on_many = models.BooleanField(default=False)

    permission = models.CharField(max_length=30, choices=PERMISSION_CHOICES, default="CAN_VIEW_PUBLIC_POLLS")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("polls_view_poll", kwargs={'poll_id': self.id})

    def can_view(self, user):
        return has_user_perm(user, self.get_permission_str())

    @staticmethod
    def can_edit(user):
     #   return has_user_perm(user, EDIT)
        return True

    def get_permission_str(self):
        return dict(PERMISSION_CHOICES)[self.permission]

    def can_user_vote(self, request):
        if request.user.is_authenticated():
            object = Votes.objects.filter(choice_id__id_to_poll=self, user=request.user)
            return not object.exists()
        else:
            return not Votes.objects.filter(choice_id__id_to_poll=self, ip_address=request.META['REMOTE_ADDR']).exists()


class Choice(models.Model):
    name = models.CharField(max_length=200)
    id_to_poll = models.ForeignKey(Poll)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("polls.views.set_user_choice", kwargs={'choice_id': self.id})

    def count_votes(self):
        return Votes.objects.filter(choice_id=self.id).count()


class Votes(models.Model):
    choice_id = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    ip_address = models.IPAddressField(default=None)

