import googlemaps
from datetime import datetime, date, time

import pandas as pd
import numpy as np
import re
import string
import csv

# Google map API's key
API_KEY = 'AIzaSyChS_xnOZ7MVdUYBgkL3b79x_WHCmggUgI'
gmaps = googlemaps.Client(key = API_KEY)


def input_date_time(user_date, user_time):
    '''
    Change the user's inputs for departure date and time into the 
    valid types which can be used in the Google map API

    Inputs:
        user_date: such as "2018,03,09"
        user_time: such as "9,26"

    Returns: a valid type for depart time in the Google map API
    '''

    year, month, day = user_date.split(',')
    hour, minute = user_time.split(',')
    d = date(int(year), int(month), int(day))
    t = time(int(hour), int(minute))

    depart_time = datetime.combine(d, t)

    return depart_time


def get_crime_time_df(user_time):
    '''
    Get the crime date subset for the specific hour, which is the user's 
    departure hour. For example, if the user enters the departure hour is
    9 am, return the "time_900_1000.csv".

    Inputs:
        user_time: such as "9,26", which means 9:26 am

    Returns: 
        A dataframe for the locations that had crimes happened at the 
        specific hour, such as all the locations which had crimes at 
        9:00-10:00 am.
    '''

    hour, minute = user_time.split(',')
    hour = int(hour)
    time_doc = str(hour * 100) + '-' + str((hour + 1) * 100)

    time_data = 'route/Data/time_' + str(time_doc) + '.csv'

    loc_weight = pd.read_csv(time_data, header=None)
    loc_weight.columns = ['loc', 'weight']
    
    return loc_weight


def build_route_dict(ori_loc, des_loc, depart_time, mode_option):
    '''
    Create a dictionary to store all the routes returned from the Google API.
    The keys are "route_1", "route_2", and so on. The values are a list of 
    steps/locations represented as a tuple: (latitude, longitude).

    Inputs:
        ori_loc: the departure location, from user's input
        des_loc: the destination location, from user's input
        depart_time: the valid depart time type for Goolge map API
        mode_option: one of "walking", “bicycling”, “driving”, or “transit”

    Returns: a dictionary for all the routes returned from API
    '''

    routes = gmaps.directions(origin = ori_loc, 
                              destination = des_loc,
                              departure_time = depart_time,
                              mode = mode_option,
                              alternatives = True)
    route_dict = {}
    for i in range(len(routes)):    
        route_name = 'route_' + str(i+1)    
        steps = routes[i]['legs'][0]['steps']     
        route_loc = []
        for j in range(len(steps)): 
            loc = steps[j]['end_location']
            loc_tuple = loc['lat'], loc['lng']
            route_loc.append(loc_tuple)     
        route_dict[route_name] = route_loc
        
    return route_dict


def build_instruction_dict(ori_loc, des_loc, depart_time, mode_option):
    '''
    Create a dictionary to store all the html direction instructions for each 
    route returned from the Google API. The keys are "route_1", "route_2"...
    The values are the html instructions, such as "Turn left", "Turn right"...

    Inputs:
        ori_loc: the departure location, from user's input
        des_loc: the destination location, from user's input
        depart_time: the valid depart time type for Goolge map API
        mode_option: one of "walking", “bicycling”, “driving”, or “transit”

    Returns: a dictionary for all the routes returned from API
    '''

    routes = gmaps.directions(origin = ori_loc, 
                              destination = des_loc,
                              departure_time = depart_time,
                              mode = mode_option,
                              alternatives = True)
    instruction_dict = {}
    for i in range(len(routes)):    
        route_name = 'route_' + str(i+1)     
        steps = routes[i]['legs'][0]['steps']     
        
        lst = []
        for j in range(len(steps)): 
            ins = steps[j]['html_instructions']
            line = '<p>' + ins + '</p >'
            lst.append(line)
        
        instruction_dict[route_name] = lst
     
    return instruction_dict


def cut_into_small_steps_helper(steps, i, diff, lat_or_lng, new_steps):
    '''
    This is a helper function for the following "cut_into_small_steps"
    function. Because the API only returns the steps/locations at the 
    corners, there are no middle steps returned between the two locations if
    they are on a straight route. Therefore, in order to check the dangerous
    situation in such a straight route as well, I divide the straight route 
    into several shorter distance by adding new steps. The distance between 
    each step is about 0.001 latitude/longitude, which is roughly a block's 
    distance. Therefore, to some degree, I have a step in each block, so I
    can check each block's dangerous level.
    
    Inputs:
        steps: a list of steps/locations returned from API
        i: the index of the "steps"
        diff: lat_diff or lng_diff in the "cut_into_small_steps" function
        lat_or_lng: an interger, 0 or 1
        new_steps: the list to store the new steps
        
    Returns: no returns, but the "new_steps" would be updated.
    '''

    new_loc = steps[i][lat_or_lng]

    n = int(diff / 0.001)
    for j in range(abs(n)):

        if diff > 0:
            new_loc += 0.001
        if diff < 0:
            new_loc -= 0.001

        if lat_or_lng == 0:
            new_step = (new_loc, steps[i][1])
        else:
            new_step = (steps[i][0], new_loc)

        new_steps.append(new_step)


def cut_into_small_steps(steps):
    '''
    This function calls the above "cut_into_small_steps_helper" function, 
    so please also read the comments for the above function. The 'if' and 
    'elif' conditions are to check the moving trend/direction. For example, 
    if lat_diff, which is the absolute difference between two locations' 
    latitudes, are larger than 0.001, and lng_diff, which is the absolute 
    difference between two locations' longitudes are smaller than 0.001, 
    we say these two steps are on a north-south (or south-north) orientational
    route. In ohter words, these two steps are on a route from up to down or 
    down to up on the map. The purpose for doing this is, in the following 
    algorithm, according to the orientational information, when a dangerous 
    step is spotted, I add a distance to this step's latitude or longitude, 
    so I get a new step on the left or the right of the dangerous step. These
    new steps may construct the potential alternative routes. 
    
    Inputs:
        steps: a list of steps/locations for the route returned from API
        
    Returns: a list of steps including the self-added steps
    '''

    new_steps = []
    for i in range(len(steps)-1):
        new_steps.append(steps[i])
        
        lat_diff = steps[i+1][0] - steps[i][0]
        lng_diff = steps[i+1][1] - steps[i][1]
        
        if (abs(lat_diff) > 0.001) & (abs(lng_diff) < 0.001):

            cut_into_small_steps_helper(steps, i, lat_diff, 0, new_steps)
            
        elif (abs(lng_diff) > 0.001) & (abs(lat_diff) < 0.001):

            cut_into_small_steps_helper(steps, i, lng_diff, 1, new_steps)
                
        else:
            continue

    new_steps.append(steps[-1])
            
    return new_steps


def enrich_routes_steps(routes):
    
    route_dict = {}
    n = len(routes)
    
    for i in range(n):    
        route_name = 'route_' + str(i+1) 
        new_steps = cut_into_small_steps(routes[route_name])
        route_dict[route_name] = new_steps
    
    return route_dict


def compute_score(time_weight, target):
    
    lat_down = target[0] - 0.0001
    lat_up = target[0] + 0.0001
    lng_left = target[1] - 0.0001
    lng_right = target[1] + 0.0001
    
    weight_dict = time_weight.set_index('loc')['weight'].to_dict()
    
    score_sum = 0
    for location in weight_dict:
        
        loc = re.findall('[+-]?\d+\.\d+', location)
        lat = float(loc[0])
        lng = float(loc[1])
        
        if (lat <= lat_up) and (lat >= lat_down) and \
           (lng >= lng_left) and (lng <= lng_right):
            
            score_sum += weight_dict[location]

    return score_sum


def compute_all_scores(time_weight, route_dict):
    
    route_score_dict = {}
    for route, loc_ls in route_dict.items():
        score_sum = 0
        
        for loc in loc_ls:           
            score = compute_score(time_weight, loc)
            score_sum += score  
        route_score_dict[route] = score_sum

    return route_score_dict 


def get_best_route(time_df, old_route_dict, new_route_dict):
    
    score_dict = compute_all_scores(time_df, new_route_dict)
    best_choice = min(score_dict, key=score_dict.get)
    best_route = old_route_dict[best_choice]
    long_best_route = new_route_dict[best_choice]
    
    return best_choice, best_route, long_best_route


def get_each_step_score(time_df, route):

    step_score = pd.DataFrame(columns = ['lat_lng', 'weight'])

    for i in range(len(route)):

        score = compute_score(time_df, route[i])

        step_score.loc[i] = [route[i], score]
        
    return step_score


def compare_routes(loc_1, loc_2, depart_time, mode_option, time_df):
    
    alter_routes = build_route_dict(loc_1, loc_2, depart_time, mode_option)                 
    new_scores = compute_all_scores(time_df, alter_routes)
    new_best_choice = min(new_scores, key=new_scores.get)
    new_best_route = alter_routes[new_best_choice]
    new_best_score = new_scores[new_best_choice]

    return new_best_route, new_best_score


def construct_alternative_route(prev_step, dangerous_step, lat_or_lng, 
                                depart_time, mode_option, time_df):
    
    new_direction_1 = dangerous_step[lat_or_lng] + 0.002
    new_direction_2 = dangerous_step[lat_or_lng] - 0.002
    
    if lat_or_lng == 1:
    
        new_step_1 = (dangerous_step[0], new_direction_1)
        new_step_2 = (dangerous_step[0], new_direction_2)
    
    else:
        new_step_1 = (new_direction_1, dangerous_step[1])
        new_step_2 = (new_direction_2, dangerous_step[1])
                
    new_route_1, new_score_1 = compare_routes(prev_step, new_step_1, 
                                              depart_time, mode_option, 
                                              time_df)
    new_route_2, new_score_2 = compare_routes(prev_step, new_step_2,
                                              depart_time, mode_option, 
                                              time_df)
    
    return new_route_1, new_score_1, new_route_2, new_score_2


def choose_safer_step(ori_step, ori_score, new_route_1, new_score_1, 
                      new_route_2, new_score_2, safe_route):
    
    min_score = ori_score
    new_route = ori_step
    
    if new_score_1 < min_score:
        min_score = new_score_1
        new_route = new_route_1
        
    elif new_score_2 < min_score:
        min_score = new_score_2
        new_route = new_route_2
    
    if new_route != ori_step:
        safe_route += new_route
    else:
        safe_route.append(ori_step)


def find_alternative_step(long_each_step_score, depart_time, mode_option, 
                          time_df):
    
    safe_route = []

    for index, row in long_each_step_score.iterrows():

        score = row.weight
        step = long_each_step_score.loc[index].lat_lng
        
        if (score != 0) & (index != max(long_each_step_score.index)):

            prev_step = long_each_step_score.loc[index-1].lat_lng
            
            if (abs(prev_step[0] - step[0]) > 0) and \
               (abs(prev_step[1] - step[1]) < 0.001):

                new_route_1, new_score_1, new_route_2, new_score_2 \
                    = construct_alternative_route(prev_step, step, 1, 
                                                  depart_time, mode_option,
                                                  time_df)
                
                choose_safer_step(step, score, new_route_1, new_score_1, 
                                  new_route_2, new_score_2, safe_route)
                
            elif (abs(prev_step[1] - step[1]) > 0) and \
                 (abs(prev_step[0] - step[0]) < 0.001):
                
                new_route_1, new_score_1, new_route_2, new_score_2 \
                    = construct_alternative_route(prev_step, step, 0, 
                                                  depart_time, mode_option,
                                                  time_df)

                choose_safer_step(step, score, new_route_1, new_score_1, 
                                  new_route_2, new_score_2, safe_route)
                
        else:
            safe_route.append(step)
            
    return safe_route


def get_route_for_map(google_route, enriched_route, altered_route):

    
    enriched_label = []
    for step in enriched_route:
        if step in google_route:
            enriched_label.append('google')
        else:
            enriched_label.append('enriched')

    enriched_df = pd.DataFrame({'step': enriched_route,
                                'label': enriched_label})

    altered_label = []
    for step in altered_route:
        if step in enriched_route:
            step_index = enriched_route.index(step)
            altered_label.append(enriched_df.label[step_index])
        else:
            altered_label.append('altered')

    altered_df = pd.DataFrame({'step': altered_route,
                               'label': altered_label})
    
    final_route = []
    for i in range(len(altered_df)):
        if altered_df.loc[i]['label'] == 'google' or \
           altered_df.loc[i]['label'] == 'altered':
            final_route.append(altered_df.loc[i]['step'])

    return final_route


def transfer_tuple_to_list(route):

    route_ls = []
    for step in route:
        route_ls.append(step[0])
        route_ls.append(step[1])

    return route_ls

