from django import forms
from django.utils.translation import ugettext as _
from exams.models import *


class ExamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['course_id'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['examinator'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = SingleExam
        fields = ('course_id', 'examinator', 'exam_date')


class ExaminatorForm(forms.ModelForm):

    class Meta:
        model = Examinator
        fields = ('name',)


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('name',)


class ExamFileForm(forms.ModelForm):

    class Meta:
        model = ExamFile
        fields = ('image',)
