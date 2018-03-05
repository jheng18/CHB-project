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
    # pts1 = [41.7913967, -87.5993036,41.791614, -87.5991562,41.7921284, -87.59884919999999,41.7923414, -87.5985792,
    #         41.7921284, -87.59884919999999,41.7916146, -87.5988321,41.7914052, -87.59854109999999,
    #         41.7914235, -87.59645069999999,41.7923444, -87.596471,41.7932285, -87.59813009999999]
    # pts1 = [41.7921284, -87.59884919999999]
    pts = [41.7932285,
           -87.59213009999996,
           41.7932285,
           -87.59113009999996,
           41.7932285,
           -87.59013009999995,
           41.7932285,
           -87.58913009999995,
           41.7932285,
           -87.58813009999994,
           41.7933449,
           -87.5878748,
           41.7943449,
           -87.5878748,
           41.795344899999996,
           -87.5878748,
           41.796344899999994,
           -87.5878748,
           41.79734489999999,
           -87.5878748,
           41.79834489999999,
           -87.5878748,
           41.79934489999999,
           -87.5878748,
           41.800344899999985,
           -87.5878748,
           41.80134489999998,
           -87.5878748,
           41.80234489999998,
           -87.5878748,
           41.8024679,
           -87.58778459999999,
           41.8024679,
           -87.58678459999999,
           41.8024679,
           -87.58578459999998,
           41.8024867,
           -87.58532489999999,
           41.8034867,
           -87.58532489999999,
           41.8037469,
           -87.5854378]
    route_option = 2
    mode_option = mode_option.swapcase()
    # return HttpResponse(org_geo)
    # return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option})
    return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option, 'pts':pts,
                                            'route_option': route_option})