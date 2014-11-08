from django import forms
from django.utils.translation import ugettext as _
from exams.models import *


class ExamForm(forms.ModelForm):

    class Meta:
        model = SingleExam
        fields = ('photo_id', 'course_id', 'ocr', 'exam_date', 'examinator')


