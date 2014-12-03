from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    year = models.IntegerField()
    photo = models.ImageField(upload_to='association/photos')
    # the board or committee name
    name = models.CharField(max_length=300)


class Role(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board)


class BoardMember(models.Model):
    board = models.ForeignKey(Board)
    role = models.ForeignKey(Role)
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to='association/photos')




