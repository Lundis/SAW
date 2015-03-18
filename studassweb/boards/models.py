from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from solo.models import SingletonModel
from members.models import Member


# Role of a board member, e.g. Chairman
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("boards_view_role", kwargs={'role_id': self.id})

    def can_delete(self):
        return not MemberInBoard.objects.filter(role=self).exists()


# The board and any committees
class BoardType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("boards_view_boardtype", kwargs={'boardtype_id': self.id})

    def get_board_count(self):
        return Board.objects.filter(boardtype=self.id).count()

    def get_member_count(self):
        # We might not need this function
        # Get all boards of this type
        all_boards = Board.objects.filter(boardtype=self.id)
        member_sum = 0
        for board in all_boards:
            member_sum += board.get_member_count()
        return member_sum

    def can_delete(self):
        return self.get_member_count() == 0


class Board(models.Model):
    year = models.IntegerField()
    photo = models.ImageField(upload_to='boards/photos', blank=True, null=True)
    boardtype = models.ForeignKey(BoardType, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.boardtype.name) + " " + str(self.year)

    def get_absolute_url(self):
        return reverse("boards_view_board", kwargs={'board_id': self.id})

    def get_member_count(self):
        return MemberInBoard.objects.filter(board=self.id).count()

    def can_delete(self):
        return self.get_member_count() == 0


class MemberInBoard(models.Model):
    board = models.ForeignKey(Board, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='boards/photos', blank=True, null=True)

    class Meta:
        unique_together = ("board", "role", "member")

    def __str__(self):
        return self.member.get_full_name()

    def get_absolute_url(self):
        return reverse("boards_view_boardmember", kwargs={'member_id': self.member.id})


class BoardSettings(SingletonModel):
    is_setup = models.BooleanField(default=False, help_text="Tells us if the first-time setup has been done")

    @classmethod
    def instance(cls):
        instance, created = cls.objects.get_or_create()
        return instance