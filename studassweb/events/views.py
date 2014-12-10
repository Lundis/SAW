from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf




def home(request):
    return render(request, "events/view_events.html")

def event_detail(request):
    return render_to_response('events/event.html')

def add_event(request):
    return render_to_response('events/add_events.html')

def attend_status(request):
    return render_to_response('events/event.html')

def edit_event(request):
    return render_to_response('events/edit_events.html')

def comment(request):
    return render_to_response('events/edit_events.html')

def archive(request):
    return render_to_response('events/archive.html')