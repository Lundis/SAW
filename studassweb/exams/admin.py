from django.contrib import admin
from .models import SingleExam, Examinator, Course, ExamFile


admin.site.register(SingleExam)
admin.site.register(ExamFile)
admin.site.register(Examinator)
admin.site.register(Course)

