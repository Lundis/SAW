from django.shortcuts import render
from django.utils.translation import ugettext as _
from exams.models import *
from gallery.models import *
from exams.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
from datetime import datetime
"""
Note that this class is completely untested and might contain horribly wrong code.
Don't use this as an example.
"""

def main(request):
    exams = SingleExam.objects.filter()
    return render(request, 'exams/view_main.html',
                  {'exams': exams},)



def view_exam(request,exam_id):
    try:
        exam = SingleExam.objects.get(id=exam_id)
        return render(request, 'exams/view_exam.html',
            {'id': exam.id, 'image': exam.image, 'course_id_id': exam.course_id.id,'course_id_name': exam.course_id.name,
            'ocr': exam.ocr, 'exam_date': exam.exam_date, 'examinator_id': exam.examinator.id, 'examinator_name': exam.examinator.name},)
    except SingleExam.DoesNotExist:
        return HttpResponseNotFound('No exam with that id found')


def view_examinator(request,examinator_id):
    #TODO show all exams by examinator
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        return render(request, 'exams/view_examinator.html',
            {'id': examinator.id, 'name': examinator.name},)
    except Examinator.DoesNotExist:
        return HttpResponseNotFound('No examinator with that id found')


def view_course(request,course_id):
    #TODO show all exams from course
    try:
        course = Course.objects.get(id=course_id)
        return render(request, 'exams/view_course.html',
            {'id': course.id, 'name': course.name},)
    except Course.DoesNotExist:
        return HttpResponseNotFound('No course with that id found')


def add_edit_exam(request, exam_id=-1):
    print("in add_edit_exam")
    form = ExamForm
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid shit")
            tmp_exam = form.save()
            return HttpResponseRedirect('/exams/exam/' + str(tmp_exam.id))
    try:
        exam = SingleExam.objects.get(id=exam_id)
        form = ExamForm(exam)
    except SingleExam.DoesNotExist:
        print("SingleExam DoesNotExist")
        pass

    context = {'form': form}
    return render(request, 'exams/add_edit_exam.html', context)


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
    return render(request, 'exams/add_edit_examinator.html', context)


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
    return render(request, 'exams/add_edit_course.html', context)