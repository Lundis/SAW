from django.db import models
from django.core.urlresolvers import reverse
from members.models import Member


#Role of a board member, e.g. Festchef
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("boards.views.view_role", kwargs={'role_id': self.id})


#Styrelsen, maskinutskottet etc.
class BoardType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("boards.views.view_boardtype", kwargs={'boardtype_id': self.id})


class Board(models.Model):
    year = models.IntegerField()
    photo = models.ImageField(upload_to='boards/photos', blank=True)
    boardtype = models.ForeignKey(BoardType, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.boardtype.name) + " " + str(self.year)

    def get_absolute_url(self):
        return reverse("boards.views.view_board", kwargs={'board_id': self.id})


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='boards/photos', blank=True)

    def __str__(self):
        return str(self.role.name) + " " + str(self.user.get_full_name())

    def get_absolute_url(self):
        return reverse("boards.views.view_boardmember", kwargs={'boardmember_id': self.id})




