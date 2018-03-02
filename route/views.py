from django.http import HttpResponse
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
    if not origin:
        # messages.add_message(request, messages.ERROR,"Error")
        messages.success(request, 'error')
        return redirect('/route/')
        # messages.add_message(request, messages.INFO, 'Please enter valid place')
        # return HttpResponseRedirect('route/index.html')
        # return reverse('route:index', args=(self.kwargs['pk'],))
        # return render_to_response('route/index.html', message='Save complete')
        # return render(request,'route/index/html')
    destin = request.GET['destination']
    destin = check(origin)
    mode = request.GET['mode']
    date = request.GET['user_date'].replace(":", ",")
    if not date:
        date = datetime.datetime.now().strftime('%Y,%m,%d')
    time = request.GET['user_time'].replace(":", ",")
    if not time:
        time = datetime.datetime.now().strftime('%H,%M')
    return HttpResponse(origin)

