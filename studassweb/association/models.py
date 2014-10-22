from django.db import models
from gallery.models import Photo
# Create your models here.

class Board(models.Model):
    year = models.IntegerField()
    photo = models.ForeignKey(Photo)
    role = models.CharField(max_length=300)


class Role(models.Model):
    name = models.CharField()
    board = models.ForeignKey(Board)

class BoardMember(models.Model):
    board = models.ForeignKey(Board)
    role = models.ForeignKey(Role)
    #User?
    photo = models.ForeignKey(Photo)

class Payment(models.Model):
    #User?
    purpose = models.CharField(max_length=200)


