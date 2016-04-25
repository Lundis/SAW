from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from users.permissions import has_user_perm
from .register import CAN_VIEW_PUBLIC_POLLS, CAN_VIEW_MEMBER_POLLS, \
    CAN_VIEW_BOARD_POLLS, CAN_VOTE_PUBLIC_POLLS, CAN_VOTE_MEMBER_POLLS, CAN_VOTE_BOARD_POLLS, CAN_EDIT_ALL_POLLS

from base.fields import ValidatedRichTextField

PERMISSION_CHOICES_VIEW = (
    (CAN_VIEW_PUBLIC_POLLS, "Everyone"),
    (CAN_VIEW_MEMBER_POLLS, "Members"),
    (CAN_VIEW_BOARD_POLLS, "The board"),
)

PERMISSION_CHOICES_VOTE = (
    (CAN_VOTE_PUBLIC_POLLS, "Everyone"),
    (CAN_VOTE_MEMBER_POLLS, "Members"),
    (CAN_VOTE_BOARD_POLLS, "The board"),
)


class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = ValidatedRichTextField(max_length=300)
    publication = models.DateTimeField('Date published', auto_now_add=True)
    expiration = models.DateTimeField('Poll closes')
    created_by = models.ForeignKey(User)
    can_vote_on_many = models.BooleanField(default=False)

    permission_choice_view = models.CharField(max_length=100, choices=PERMISSION_CHOICES_VIEW,
                                              verbose_name="Who can view this poll?",
                                              default="CAN_VIEW_PUBLIC_POLLS")
    permission_choice_vote = models.CharField(max_length=100, choices=PERMISSION_CHOICES_VOTE,
                                              verbose_name="Who can vote on this poll?",
                                              default="CAN_VOTE_PUBLIC_POLLS")

    def count_votes(self):
        return Vote.objects.filter(choice_id__id_to_poll=self).count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("polls_view_poll", kwargs={'poll_id': self.id})

    def can_view(self, user):
        return has_user_perm(user, self.permission_choice_view)

    def can_edit(self, user):
        return self.created_by == user or has_user_perm(user, CAN_EDIT_ALL_POLLS)

    def can_user_vote(self, request):
        if not has_user_perm(request.user, self.permission_choice_vote):
            return False
        if request.user.is_authenticated():
            object = Vote.objects.filter(choice_id__id_to_poll=self, user=request.user)
            return not object.exists()
        else:
            return not Vote.objects.filter(choice_id__id_to_poll=self, ip_address=request.META['REMOTE_ADDR']).exists()

    def has_user_voted(self, request):
        return not self.can_user_vote(request) #TODO STUFF ENNU NOGO


class Choice(models.Model):
    name = models.CharField(max_length=200, verbose_name="Option")
    id_to_poll = models.ForeignKey(Poll)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("polls.views.set_user_choice", kwargs={'choice_id': self.id})

    def count_votes(self):
        return Vote.objects.filter(choice_id=self.id).count()

    def percentage(self):
        total_votes_for_poll = self.id_to_poll.count_votes()
        total_votes_for_specific_choice = Vote.objects.filter(choice_id=self).count()
        if total_votes_for_poll == 0:
            total_votes_for_poll = 1
        percent = total_votes_for_specific_choice/total_votes_for_poll
        return percent*100


class Vote(models.Model):
    choice_id = models.ForeignKey(Choice)
    user = models.ForeignKey(User, null=True)
    ip_address = models.GenericIPAddressField(default=None)



