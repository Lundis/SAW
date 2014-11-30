from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("exams.views.view_course", kwargs={'course_id': self.id})

    def get_exam_count(self):
        return str(SingleExam.objects.filter(course_id=self.id).count())


class Examinator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exams.views.view_examinator", kwargs={'examinator_id': self.id})

    def get_exam_count(self):
        return str(SingleExam.objects.filter(examinator=self.id).count())


class SingleExam(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)
    ocr = models.TextField(blank=True)
    exam_date = models.DateTimeField()
    examinator = models.ForeignKey(Examinator, on_delete=models.PROTECT)

    def __str__(self):
        return self.exam_date.strftime("%Y-%m-%d") + " : " + str(self.examinator) + " : " + str(self.course_id)

    def get_absolute_url(self):
        return reverse("exams.views.view_exam", kwargs={'exam_id': self.id})


class ExamFile(models.Model):
    image = models.ImageField(upload_to='exams_files')
    exam_id = models.ForeignKey(SingleExam)

    def __str__(self):
        return self.image.name





