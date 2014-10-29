from django.db import models
from gallery.models import Photo
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    year = models.IntegerField()
    photo = models.ForeignKey(Photo)
    # the board or committee name
    name = models.CharField(max_length=300)


class Role(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board)

class BoardMember(models.Model):
    board = models.ForeignKey(Board)
    role = models.ForeignKey(Role)
    person_id = models.ForeignKey(User)  # IS THIS SUPPOUSE TO BE SAME FOREIGN KEY?
    photo = models.ForeignKey(Photo)

class Payment(models.Model):
    user = models.ForeignKey(User)
    purpose = models.CharField(max_length=200)


