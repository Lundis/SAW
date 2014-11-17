from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Examinator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SingleExam(models.Model):
    course_id = models.ForeignKey(Course)
    ocr = models.TextField(blank=True)
    exam_date = models.DateTimeField()
    examinator = models.ForeignKey(Examinator)

    def __str__(self):
        return str(self.exam_date) + " : " + str(self.examinator) + " : " + str(self.course_id)


class ExamFile(models.Model):
    image = models.ImageField(upload_to='exams_files')
    exam_id = models.ForeignKey(SingleExam)

    def __str__(self):
        return self.image.name





