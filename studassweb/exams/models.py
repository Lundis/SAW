from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("exams.views.view_course", kwargs={'course_id': self.id})

    def get_exam_count(self):
        return str(SingleExam.objects.filter(course_id=self.id).count())


class Examinator(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
    examinator = models.ForeignKey(Examinator, on_delete=models.PROTECT, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.exam_date.strftime("%Y-%m-%d") + " : " + str(self.examinator_with_default_values) + " : " + str(self.course_id)

    def get_absolute_url(self):
        return reverse("exams.views.view_exam", kwargs={'exam_id': self.id})

    @property
    def examinator_with_default_values(self):
        if self.examinator:
            return self.examinator
        else:
            return Examinator(name="Unknown examinator")


class ExamFile(models.Model):
    image = models.ImageField(upload_to='exams_files')
    exam_id = models.ForeignKey(SingleExam)

    def __str__(self):
        return self.image.name





