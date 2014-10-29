from django.db import models

from gallery.models import Photo


class Course(models.Model):
    name = models.CharField(max_length=100)


class Examinator(models.Model):
    name = models.CharField(max_length=100)


class SingleExam(models.Model):
    photo_id = models.ForeignKey(Photo)
    course_id = models.ForeignKey(Course)
    ocr = models.TextField()
    exam_date = models.DateTimeField()
    examinator = models.ForeignKey(Examinator)








