from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'example.views.choose', name='examplechoose'),
    # (\d) means that it will match a single digit and pass it to the view function
    url(r'(\d+)', 'example.views.result', name='exampleresult'),
)
