from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response,redirect
import datetime, json
# from .models import PointOfInterest
from django.urls import reverse
from django import forms
from django.contrib import messages

from route.checkplace import *


from route.Compute_crime_weights import *
# from route.main import *
from route.Subset_date_by_time import *

import route.Choose_safest_route as csr



def index(request):
    return render(request, 'route/index.html')

def map(request):
    origin = request.GET['origin']
    origin = check(origin)[0]
    org_geo = check(origin)[1]
    # if not origin:
    #     messages.error(request, 'error')
    #     return render(request, 'route/index.html')
    destin = request.GET['destination']
    destin = check(destin)[0]
    des_geo = check(destin)[1]
    if not destin or not origin or (origin == destin):
        messages.error(request, 'Please enter a valid address.')
        return HttpResponseRedirect( reverse('type') )
    mode_option = request.GET['mode']
    d = request.GET['user_date'].replace("-", ",")
    today = datetime.datetime.now().strftime('%Y,%m,%d')
    t = request.GET['user_time'].replace(":", ",")
    right_moment = datetime.datetime.now().strftime('%H,%M')
    if not t:
        t = right_moment
    if not d:
        d = today
    if d < today:
        d = today
        if t < right_moment:
            t = right_moment
    t = t[0].strip('0') + t[1:]
    mode_option = mode_option.swapcase()
    pts = []
    route_option = 1
    # pts = [41.7913123, -87.6061636, 41.7913123, -87.6051636, 41.7913123, -87.60416359999999, 41.7913123, -87.60316359999999, 41.791358, -87.60249639999999, 41.7909978, -87.6024699, 41.7899978, -87.6024699, 41.7894855, -87.6015256, 41.7892259, -87.60152049999999, 41.7892299, -87.60072249999999, 41.788229900000005, -87.60072249999999, 41.78774200000001, -87.6005843, 41.78774200000001, -87.59958429999999, 41.7877494, -87.59957589999999]
    # return HttpResponse(des_geo)
    # return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option})
    return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option, 'pts':pts,
                                            'route_option': route_option})
    # return render(request, 'route/map.html', {'pts':pts, 'mode_option': mode_option})
    # return render(request, 'route/map.html', {'pts':pts,'mode_option': mode_option})