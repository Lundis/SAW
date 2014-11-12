from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',                                      'exams.views.main',                 name='exams_main'),
    url(r'^exam/(?P<exam_id>\d+)$',                 'exams.views.view_exam',            name='exams_view_exam'),
    url(r'^examinator/(?P<examinator_id>\d+)$',     'exams.views.view_examinator',      name='exams_view_examinator'),
    url(r'^course/(?P<course_id>\d+)$',             'exams.views.view_course',          name='exams_view_course'),
    url(r'^add_exam/$',                             'exams.views.add_edit_exam',        name='exams_add_exam'),
    url(r'^add_examinator/$',                       'exams.views.add_edit_examinator',  name='exams_add_examinator'),
    url(r'^add_course/$',                           'exams.views.add_edit_course',      name='exams_add_course'),
    url(r'^edit_exam/(?P<exam_id>\d+)$',            'exams.views.add_edit_exam',        name='exams_edit_exam'),
    url(r'^edit_examinator/(?P<examinator_id>\d+)$','exams.views.add_edit_examinator',  name='exams_edit_examinator'),
    url(r'^edit_course/(?P<course_id>\d+)$',        'exams.views.add_edit_course',      name='exams_edit_course'),
)

