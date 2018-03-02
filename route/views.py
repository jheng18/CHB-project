from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from utilies_dir import algorithm
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
    if not destin or not origin:
        messages.error(request, '2Error message here')
        return HttpResponseRedirect( reverse('route') )
    mode = request.GET['mode']
    date = request.GET['user_date'].replace(":", ",")
    if not date:
        date = datetime.datetime.now().strftime('%Y,%m,%d')
    time = request.GET['user_time'].replace(":", ",")
    if not time:
        time = datetime.datetime.now().strftime('%H,%M')
    # return render(request, 'route/map.html', {'form': form})
    return render(request, 'route/map.html', context={"needall":[origin,destin,mode,date,time]})