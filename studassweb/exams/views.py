from django.shortcuts import render
from django.utils.translation import ugettext as _
from exams.models import *
from exams.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.forms.models import inlineformset_factory


def main(request):
    exams = SingleExam.objects.filter().order_by('-exam_date')
    courses = Course.objects.filter().order_by('name')
    examinators = Examinator.objects.filter().order_by('name')
    return render(request, 'exams/view_main.html',
                  {'exams': exams, 'courses': courses, 'examinators': examinators},)


def view_exam(request, exam_id):
    try:
        exam = SingleExam.objects.get(id=exam_id)
        images = ExamFile.objects.filter(exam_id=exam_id)

        return render(request, 'exams/view_exam.html', {
            'exam': exam, 'images': images},)
    except SingleExam.DoesNotExist:
        return HttpResponseNotFound('No exam with that id found')


def view_examinator(request, examinator_id):
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        exams = SingleExam.objects.filter(examinator=examinator_id).order_by('-exam_date')
        return render(request, 'exams/view_examinator.html', {
            'examinator': examinator, 'exams': exams},)
    except Examinator.DoesNotExist:
        return HttpResponseNotFound('No examinator with that id found')


def view_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        exams = SingleExam.objects.filter(course_id=course_id).order_by('-exam_date')
        return render(request, 'exams/view_course.html', {
            'course': course, 'exams': exams},)
    except Course.DoesNotExist:
        return HttpResponseNotFound('No course with that id found')


def add_edit_exam(request, exam_id=-1):
    form = ExamForm()
    examfile_factory = inlineformset_factory(SingleExam, ExamFile, fields=('id', 'image',), extra=1, can_delete=True)
    try:
        exam = SingleExam.objects.get(id=exam_id)
        form = ExamForm(instance=exam)
        fileformset = examfile_factory(instance=exam, prefix='dynamix')
    except SingleExam.DoesNotExist:
        fileformset = examfile_factory(prefix='dynamix')
        exam = None

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)

        fileformset = examfile_factory(request.POST, request.FILES, instance=exam, prefix='dynamix')
        if form.is_valid() and fileformset.is_valid():
            tmpexam = form.save()

            for obj in fileformset.save(commit=False):
                obj.exam_id = tmpexam
                obj.save()

            for obj in fileformset.deleted_objects:
                obj.delete()

            return HttpResponseRedirect('/exams/exam/' + str(tmpexam.id))

    context = {'form': form, 'filesformset': fileformset}
    return render(request, 'exams/add_edit_exam.html', context)


def add_edit_examinator(request, examinator_id=-1):
    try:
        examinator = Examinator.objects.get(id=examinator_id)
    except Examinator.DoesNotExist:
        examinator = None
    form = ExaminatorForm(instance=examinator)

    if request.method == 'POST':
        form = ExaminatorForm(request.POST, instance=examinator)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect('/exams/examinator/' + str(tmp.id))

    context = {'form': form}
    return render(request, 'exams/add_edit_examinator.html', context)


def add_edit_course(request, course_id=-1):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        course = None
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect('/exams/course/' + str(tmp.id))

    context = {'form': form}
    return render(request, 'exams/add_edit_course.html', context)


def delete_exam(request, exam_id):
    if request.method == 'POST':
        try:
            exam = SingleExam.objects.get(id=exam_id)
            images = ExamFile.objects.filter(exam_id=exam_id)
            images.delete()
            exam.delete()
            return HttpResponseRedirect('/exams/')
        except SingleExam.DoesNotExist:
            return HttpResponseNotFound('No such exam!')


def delete_examinator(request, examinator_id):
    if request.method == 'POST':
        try:
            examinator = Examinator.objects.get(id=examinator_id)
            examinator.delete()
            return HttpResponseRedirect('/exams/')
        except Examinator.DoesNotExist:
            return HttpResponseNotFound('No such examinator!')
        except models.ProtectedError:
            return HttpResponseNotFound('You need to remove associated exams first')


def delete_course(request, course_id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return HttpResponseRedirect('/exams/')
        except Course.DoesNotExist:
            return HttpResponseNotFound('No such course!')
        except models.ProtectedError:
            return HttpResponseNotFound('You need to remove associated exams first')