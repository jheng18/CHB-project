from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response,redirect
import datetime
from route.checkplace import *
# from .models import PointOfInterest
from django.urls import reverse
from django import forms
from django.contrib import messages

# from route.Choose_safest_route import *
from route.Compute_crime_weights import *
# from route.main import *
from route.Subset_date_by_time import *

import route.Choose_safest_route as csr





def index(request):
    return render(request, 'route/index.html')

def map(request):
    origin = request.GET['origin']
    origin = check(origin)
    destin = request.GET['destination']
    destin = check(destin)
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
    depart_time = csr.input_date_time(d, t)
    loc_weight = csr.get_crime_time_df(t)
    return render_template("map.html", name=filename, data=loc_weight)
    # route_dict = csr.build_route_dict(origin, destin, depart_time, mode_option)
    # instruction_dict = csr.build_instruction_ls(origin, destin, depart_time,mode_option)
    # long_route_dict = csr.enrich_routes_steps(route_dict)
    # return HttpResponse(loc_weight)
    # return render(request, 'route/map.html', {'org':origin, 'des':destin, 'mode_option': mode_option})