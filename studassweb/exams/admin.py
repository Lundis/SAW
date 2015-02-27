from django.contrib import admin
from .models import Exam, Examinator, Course, ExamFile


admin.site.register(Exam)
admin.site.register(ExamFile)
admin.site.register(Examinator)
admin.site.register(Course)

