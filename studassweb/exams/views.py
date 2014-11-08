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
    exams = SingleExam.objects.filter(id=exam_id)
    if len(exams) > 0:
        exam = SingleExam.getById(exam_id)
        return render(request,'exam/view_exam.html',
            {'id': exam.id, 'photo_id': exam.photo_id, 'course_id': exam.photo_id,
            'ocr': exam.ocr, 'exam_date': exam.exam_date, 'examinator': exam.examinator},)
    else:
        return HttpResponseNotFound('No exam with that id found')


def view_examinator(request,examinator_id):
    #TODO show all exams by examinator
    examinators = SingleExam.objects.filter(id=examinator_id)
    if len(examinators) > 0:
        examinator = SingleExam.getById(examinator_id)
        return render(request,'exam/view_examinator.html',
            {'id': examinator.id, 'name': examinator.name},)
    else:
        return HttpResponseNotFound('No examinator with that id found')


def view_course(request,course_id):
    #TODO show all exams from course
    courses = SingleExam.objects.filter(id=course_id)
    if len(courses) > 0:
        course = SingleExam.getById(course_id)
        return render(request,'exam/view_course.html',
            {'id': course.id, 'name': course.name},)
    else:
        return HttpResponseNotFound('No course with that id found')


def add_edit_exam(request, exam_id=-1):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        #TODO return to saved exam
        return HttpResponseRedirect('/exams/')
    try:
        exam = SingleExam.objects.get(id=exam_id)
        form = ExamForm(exam)
    except SingleExam.DoesNotExist:
        pass

    context = {'form': form}
    return render(request, 'add_edit_exam.html', context)



def add_edit_examinator(request,examinator_id):
    return HttpResponseNotFound('add_edit__examinator(): function not implemented')


def add_edit_course(request,course_id):
    return HttpResponseNotFound('add_edit__course(): function not implemented')