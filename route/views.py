from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response,redirect
import datetime, json
from django.urls import reverse
from django import forms
from django.contrib import messages
from route.checkplace import *
import route.Choose_safest_route as csr


def index(request):
    return render(request, 'route/index.html')

# Reference:
# https://stackoverflow.com/questions/27753574/python-remove-first-number-from-string-if-its-0
def map(request):
    '''
    Get users input and show routes on route/map.html.

    If users provide an invlid address, they will be redirect to route/index.html and receive an error message.
    The algorithm only works on future dates and time, so we set default values as current time and dates. If users
    choose past time and date, we will use the default values.

    Returns:
         pts: a list of waypoints that a safe route will pass
         mode_option: choosen mode option
    '''
    origin = request.GET['origin']
    # check if address valid
    origin = check(origin)[0]
    destin = request.GET['destination']
    # check if address valid
    destin = check(destin)[0]
    # show message
    if not destin or not origin:
        messages.error(request, 'Please enter a valid address.')
        return HttpResponseRedirect( reverse('type') )
    if destin==origin:
        messages.error(request, 'Please enter different addresses for origin place and destination.')
        return HttpResponseRedirect( reverse('type') )
    else:
        org_geo = check(origin)[1]
        des_geo = check(destin)[1]

    mode_option = request.GET['mode']

    # check if user_date and user_time are future dates and time
    user_date = request.GET['user_date'].replace("-", ",")
    today = datetime.datetime.now().strftime('%Y,%m,%d')
    user_time = request.GET['user_time'].replace(":", ",")
    right_moment = datetime.datetime.now().strftime('%H,%M')
    if not user_time:
        user_time = right_moment
    if not user_date:
        user_date = today
    if user_date <= today:
        user_date = today
        if user_time < right_moment:
            user_time = right_moment
    # delete start 0 for time
    user_time = user_time[0].strip('0') + user_time[1:]

    pts = org_geo

    depart_time = csr.input_date_time(user_date, user_time)
    loc_weight = csr.get_crime_time_df(user_time)
    google_route_dict = csr.build_route_dict(origin, destin, depart_time, mode_option)
    instruction_dict = csr.build_instruction_dict(origin, destin, depart_time, mode_option)
    enriched_route_dict = csr.enrich_routes_steps(google_route_dict)
    best_choice, google_route, enriched_route = csr.get_best_route(loc_weight, google_route_dict, enriched_route_dict)
    google_each_step_score = csr.get_each_step_score(loc_weight, google_route)
    enriched_each_step_score = csr.get_each_step_score(loc_weight, enriched_route)
    altered_route = csr.find_alternative_step(enriched_each_step_score, depart_time, mode_option, loc_weight)
    final_route = csr.get_route_for_map(google_route, enriched_route, altered_route)
    google_route_ls = csr.transfer_tuple_to_list(google_route)
    enriched_route_ls = csr.transfer_tuple_to_list(enriched_route)
    altered_route_ls = csr.transfer_tuple_to_list(altered_route)
    final_route_ls = csr.transfer_tuple_to_list(final_route)

    pts += final_route_ls
    pts += des_geo
    # google javascript api takes uppercase mode option, whereas direction api takes lowercase.
    mode_option = mode_option.swapcase()
    return render(request, 'route/map.html', {'pts':pts,'mode_option': mode_option})
