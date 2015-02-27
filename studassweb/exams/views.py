from django.shortcuts import render
from django.utils.translation import ugettext as _
from exams.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.forms.models import inlineformset_factory
from users import permissions
from .register import CAN_VIEW_EXAM_ARCHIVE, CAN_UPLOAD_EXAMS, CAN_EDIT_EXAMS
from users.decorators import has_permission
from django.core.urlresolvers import reverse
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


@has_permission(CAN_VIEW_EXAM_ARCHIVE)
def main(request):
    exams = Exam.objects.filter().order_by('-exam_date')
    courses = Course.objects.filter().order_by('name')
    examinators = Examinator.objects.filter().order_by('name')

    return render(request, 'exams/view_main.html', {'exams': exams, 'courses': courses, 'examinators': examinators},)


@has_permission(CAN_VIEW_EXAM_ARCHIVE)
def view_exam(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        images = ExamFile.objects.filter(exam_id=exam_id)

        return render(request, 'exams/view_exam.html', {'exam': exam, 'images': images},)
    except Exam.DoesNotExist:
        logger.warning('Could not find exam with id %s', exam_id)
        return HttpResponseNotFound(_('No exam with that id found'))


@has_permission(CAN_VIEW_EXAM_ARCHIVE)
def view_examinator(request, examinator_id):
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        exams = Exam.objects.filter(examinator=examinator_id).order_by('-exam_date')

        return render(request, 'exams/view_examinator.html', {'examinator': examinator, 'exams': exams},)
    except Examinator.DoesNotExist:
        logger.warning('Could not find examinator with id %s', examinator_id)
        return HttpResponseNotFound(_('No examinator with that id found'))


@has_permission(CAN_VIEW_EXAM_ARCHIVE)
def view_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        exams = Exam.objects.filter(course_id=course_id).order_by('-exam_date')

        return render(request, 'exams/view_course.html', {'course': course, 'exams': exams},)
    except Course.DoesNotExist:
        logger.warning('Could not find course with id %s', course_id)
        return HttpResponseNotFound(_('No course with that id found'))


def add_edit_exam(request, exam_id=-1):
    form = ExamForm()
    examfile_factory = inlineformset_factory(Exam, ExamFile, fields=('id', 'image',), extra=1, can_delete=True)
    try:
        exam = Exam.objects.get(id=exam_id)
        if not (permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or exam.created_by == request.user):
            logger.warning('User %s tried to edit exam %s', request.user, exam_id)
            return HttpResponseForbidden(_('You don\'t have permission to edit this exam!'))
        form = ExamForm(instance=exam)
        fileformset = examfile_factory(instance=exam, prefix='dynamix')
    except Exam.DoesNotExist:
        if not permissions.has_user_perm(request.user, CAN_UPLOAD_EXAMS):
                logger.warning('User %s tried to add exam', request.user)
                return HttpResponseForbidden(_('You don\'t have permission to add exams!'))
        fileformset = examfile_factory(prefix='dynamix')
        exam = None

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)

        fileformset = examfile_factory(request.POST, request.FILES, instance=exam, prefix='dynamix')
        if form.is_valid() and fileformset.is_valid():
            tmpexam = form.save(commit=False)
            tmpexam.created_by = request.user
            tmpexam.save()

            for obj in fileformset.save(commit=False):
                obj.exam_id = tmpexam
                obj.save()

            for obj in fileformset.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse("exams_view_exam", args=[tmpexam.id]))

    context = {'form': form, 'filesformset': fileformset}
    return render(request, 'exams/add_edit_exam.html', context)


def add_edit_examinator(request, examinator_id=-1):
    try:
        examinator = Examinator.objects.get(id=examinator_id)
        if not (permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or examinator.created_by == request.user):
            logger.warning('User %s tried to edit examinator %s', request.user, examinator_id)
            return HttpResponseForbidden(_('You don\'t have permission to edit this examinator!'))
    except Examinator.DoesNotExist:
        examinator = None
        if not permissions.has_user_perm(request.user, CAN_UPLOAD_EXAMS):
            logger.warning('User %s tried to add examinator', request.user)
            return HttpResponseForbidden(_('You don\'t have permission to add examinators!'))
    form = ExaminatorForm(instance=examinator)

    if request.method == 'POST':
        form = ExaminatorForm(request.POST, instance=examinator)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.created_by = request.user
            tmp.save()
            return HttpResponseRedirect(reverse("exams_view_examinator", args=[tmp.id]))

    context = {'form': form}
    return render(request, 'exams/add_edit_examinator.html', context)


def add_edit_course(request, course_id=-1):
        try:
            course = Course.objects.get(id=course_id)
            if not (permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or course.created_by == request.user):
                logger.warning('User %s tried to edit course %s', request.user, course_id)
                return HttpResponseForbidden(_('You don\'t have permission to edit this course!'))
        except Course.DoesNotExist:
            course = None
            if not permissions.has_user_perm(request.user, CAN_UPLOAD_EXAMS):
                logger.warning('User %s tried to add course', request.user)
                return HttpResponseForbidden(_('You don\'t have permission to add courses!'))
        form = CourseForm(instance=course)

        if request.method == 'POST':
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.created_by = request.user
                tmp.save()
                return HttpResponseRedirect(reverse("exams_view_course", args=[tmp.id]))

        context = {'form': form}
        return render(request, 'exams/add_edit_course.html', context)


def delete_exam(request, exam_id):
        if request.method == 'POST':
            try:
                exam = Exam.objects.get(id=exam_id)
                if permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or exam.created_by == request.user:
                    name = str(exam)
                    images = ExamFile.objects.filter(exam_id=exam_id)
                    images.delete()
                    exam.delete()
                    messages.success(request, _("Exam "+name+" was sucessfully deleted!"))
                    return HttpResponseRedirect(reverse("exams_main"))
                else:
                    logger.warning('User %s tried to delete exam %s', request.user, exam_id)
                    return HttpResponseForbidden(_('You don\'t have permission to remove this!'))
            except Exam.DoesNotExist:
                return HttpResponseNotFound(_('No such exam!'))
        else:
            logger.warning('Attempted to access delete_exam via GET')
            return HttpResponseNotAllowed(['POST', ])


def delete_examinator(request, examinator_id):
    if request.method == 'POST':
        try:
            examinator = Examinator.objects.get(id=examinator_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or examinator.created_by == request.user:
                name = str(examinator)
                examinator.delete()
                messages.success(request, _("Examinator "+name+" was sucessfully deleted!"))
                return HttpResponseRedirect(reverse("exams_main"))
            else:
                logger.warning('User %s tried to delete examinator %s', request.user, examinator_id)
                return HttpResponseForbidden(_('You don\'t have permission to remove this!'))
        except Examinator.DoesNotExist:
            return HttpResponseNotFound(_('No such examinator!'))
        except models.ProtectedError:
            return HttpResponseNotFound(_('You need to remove associated exams first'))
    else:
            logger.warning('Attempted to access delete_examinator via GET')
            return HttpResponseNotAllowed(['POST', ])


def delete_course(request, course_id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(id=course_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_EXAMS) or course.created_by == request.user:
                name = str(course)
                course.delete()
                messages.success(request, _("Course "+name+" was sucessfully deleted!"))
                return HttpResponseRedirect(reverse("exams_main"))
            else:
                logger.warning('User %s tried to delete course %s', request.user, course_id)
                return HttpResponseForbidden(_('You don\'t have permission to remove this!'))
        except Course.DoesNotExist:
            return HttpResponseNotFound(_('No such course!'))
        except models.ProtectedError:
            return HttpResponseNotFound(_('You need to remove associated exams first'))
    else:
            logger.warning('Attempted to access delete_course via GET')
            return HttpResponseNotAllowed(['POST', ])