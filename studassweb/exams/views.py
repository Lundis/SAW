from django.shortcuts import render
from django.utils.translation import ugettext as _
from exams.models import *
from exams.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.forms.models import inlineformset_factory


def main(request):
    exams = SingleExam.objects.filter()
    return render(request, 'exams/view_main.html',
                  {'exams': exams},)


def view_exam(request, exam_id):
    try:
        exam = SingleExam.objects.get(id=exam_id)
        images = ExamFile.objects.filter(exam_id=exam_id)

        return render(request, 'exams/view_exam.html', {
            'id': exam.id, 'images': images, 'course_id_id': exam.course_id.id, 'course_id_name': exam.course_id.name,
            'ocr': exam.ocr, 'exam_date': exam.exam_date, 'examinator_id': exam.examinator.id,
            'examinator_name': exam.examinator.name},)
    except SingleExam.DoesNotExist:
        return HttpResponseNotFound('No exam with that id found')


def view_examinator(request, examinator_id):
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        exams = SingleExam.objects.filter(examinator=examinator_id).order_by('-exam_date')
        return render(request, 'exams/view_examinator.html', {
            'id': examinator.id, 'name': examinator.name, 'exams': exams},)
    except Examinator.DoesNotExist:
        return HttpResponseNotFound('No examinator with that id found')


def view_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        exams = SingleExam.objects.filter(course_id=course_id).order_by('-exam_date')
        return render(request, 'exams/view_course.html', {
            'id': course.id, 'name': course.name, 'exams': exams},)
    except Course.DoesNotExist:
        return HttpResponseNotFound('No course with that id found')


def add_edit_exam(request, exam_id=-1):
    form = ExamForm()
    examfile_factory = inlineformset_factory(SingleExam, ExamFile)
    exam = SingleExam
    try:
        exam = SingleExam.objects.get(id=exam_id)
        form = ExamForm(instance=exam)
        fileformset = examfile_factory(instance=exam)
    except SingleExam.DoesNotExist:
        fileformset = examfile_factory()
        pass

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)

        fileFormSet = examfile_factory(request.POST, request.FILES, instance=exam)
        if form.is_valid() and fileFormSet.is_valid():
            tmpexam = form.save()

            for obj in fileFormSet.save(commit=False):
                obj.exam_id = tmpexam
                obj.save()

            for obj in fileFormSet.deleted_objects:
                obj.delete()

            return HttpResponseRedirect('/exams/exam/' + str(tmpexam.id))

    context = {'form': form, 'filesformset': fileformset}
    return render(request, 'exams/add_edit_exam.html', context)


def add_edit_examinator(request, examinator_id=-1):
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


def add_edit_course(request, course_id=-1):
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