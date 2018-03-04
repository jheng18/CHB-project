from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response,redirect
import datetime
# from .models import PointOfInterest
from django.urls import reverse
from django import forms
from django.contrib import messages

from route.checkplace import *

def index(request):
    return render(request, 'route/index.html')

def map(request):
    origin = request.GET['origin']
    origin = check(origin)
    # if not origin:
    #     messages.error(request, 'error')
    #     return render(request, 'route/index.html')
    destin = request.GET['destination']
    destin = check(destin)
    if not destin or not origin or (origin == destin):
        messages.error(request, 'Please enter a valid address.')
        return HttpResponseRedirect( reverse('type') )
    mode_option = request.GET['mode']
    d = request.GET['user_date'].replace(":", ",")
    if not d:
        d = datetime.datetime.now().strftime('%Y,%m,%d')
    t = request.GET['user_time'].replace(":", ",")
    if not t:
        t = datetime.datetime.now().strftime('%H,%M')
    # return render(request, 'route/map.html', {'form': form})
    # mydic = {'org':origin, 'des':destin, 'mode_option': mode_option}
    # return HttpResponse(origin)
    return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option})