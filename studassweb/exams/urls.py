from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                                      views.main,                 name='exams_main'),
    url(r'^exam/(?P<exam_id>\d+)$',                 views.view_exam,            name='exams_view_exam'),
    url(r'^examinator/(?P<examinator_id>\d+)$',     views.view_examinator,      name='exams_view_examinator'),
    url(r'^course/(?P<course_id>\d+)$',             views.view_course,          name='exams_view_course'),
    url(r'^add_exam/$',                             views.add_edit_exam,        name='exams_add_exam'),
    url(r'^add_examinator/$',                       views.add_edit_examinator,  name='exams_add_examinator'),
    url(r'^add_course/$',                           views.add_edit_course,      name='exams_add_course'),
    url(r'^edit_exam/(?P<exam_id>\d+)$',            views.add_edit_exam,        name='exams_edit_exam'),
    url(r'^edit_examinator/(?P<examinator_id>\d+)$', views.add_edit_examinator,  name='exams_edit_examinator'),
    url(r'^edit_course/(?P<course_id>\d+)$',        views.add_edit_course,      name='exams_edit_course'),
    url(r'^delete_exam/(?P<exam_id>\d+)$',            views.delete_exam,        name='exams_delete_exam'),
    url(r'^delete_examinator/(?P<examinator_id>\d+)$', views.delete_examinator,  name='exams_delete_examinator'),
    url(r'^delete_course/(?P<course_id>\d+)$',        views.delete_course,      name='exams_delete_course'),
]

