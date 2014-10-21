from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def welcome(request):
    pass

@login_required
def association(request):
    pass

@login_required
def modules(request):
    pass

@login_required
def menu(request):
    pass

@login_required
def finished(request):
    pass