from django.shortcuts import render
from django.utils.translation import ugettext as _
from exams.models import *
from exams.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
"""
Note that this class is completely untested and might contain horribly wrong code.
Don't use this as an example.
"""

def main(request):
    return HttpResponseNotFound('main(): function not implemented')


def view_exam(request,exam_id):
    try:
        exam = SingleExam.objects.get(id=exam_id)
        return render(request,'view_exam.html',
            {'id': exam.id, 'photo_id': exam.photo_id, 'course_id': exam.photo_id,
            'ocr': exam.ocr, 'exam_date': exam.exam_date, 'examinator': exam.examinator},)
    except SingleExam.DoesNotExist:
        return HttpResponseNotFound('No exam with that id found')


def view_examinator(request,examinator_id):
    #TODO show all exams by examinator
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        return render(request,'view_examinator.html',
            {'id': examinator.id, 'name': examinator.name},)
    except Examinator.DoesNotExist:
        return HttpResponseNotFound('No examinator with that id found')


def view_course(request,course_id):
    #TODO show all exams from course
    try:
        course = Course.objects.get(id=course_id)
        return render(request,'view_course.html',
            {'id': course.id, 'name': course.name},)
    except Course.DoesNotExist:
        return HttpResponseNotFound('No course with that id found')


def add_edit_exam(request, exam_id=-1):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        tmp = form.save()
        return HttpResponseRedirect('/exams/exam/' + str(tmp.id))
    try:
        exam = SingleExam.objects.get(id=exam_id)
        form = ExamForm(exam)
    except SingleExam.DoesNotExist:
        pass

    context = {'form': form}
    return render(request, 'add_edit_exam.html', context)


def add_edit_examinator(request,examinator_id=-1):
    form = ExaminatorForm(request.POST or None)
    if form.is_valid():
        tmp = form.save()
        return HttpResponseRedirect('/exams/examinator/' + str(tmp.id))
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        form = ExaminatorForm(examinator)
    except Examinator.DoesNotExist:
        pass

    context = {'form': form}
    return render(request, 'add_edit_examinator.html', context)


def add_edit_course(request,course_id=-1):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        tmp = form.save()
        return HttpResponseRedirect('/exams/course/' + str(tmp.id))
    try:
        course = Examinator.objects.get(id=course_id)
        form = CourseForm(course)
    except Examinator.DoesNotExist:
        pass

    context = {'form': form}
    return render(request, 'add_edit_course.html', context)