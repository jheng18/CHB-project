import csv
import pandas as pd
import numpy as np
import re
import string

import Choose_safest_route as csr


if __name__ == "__main__":

    user_date = "2018,03,07"
    user_time = "18,45"
    mode_option = 'walking'

    # ori_loc = 'Regenstein Library, East 57th Street, Chicago, IL, USA'
    # des_loc = 'Regents Park, South East End Avenue, Chicago, IL, USA'
    # ori_loc = '4907 S Cottage Grove Ave, Chicago, IL 60615'
    # des_loc = 'Harper Memorial Library, 1116 E 59th St, Chicago, IL 60637'
    # ori_loc = '900-906 E 53rd St, Chicago, IL 60615'
    # des_loc = '5800 S Woodlawn Ave, Chicago, IL 60637'
    # ori_loc = '4756 S Forrestville Ave, Chicago, IL 60615'
    # des_loc = '1398 E 58th St, Chicago, IL 60637'
    ori_loc = '4756 S Vincennes Ave, Chicago, IL 60615'
    des_loc = '1499 E 57th St, Chicago, IL 60637'


    depart_time = csr.input_date_time(user_date, 
                                      user_time)

    loc_weight = csr.get_crime_time_df(user_time)

    google_route_dict = csr.build_route_dict(ori_loc, 
                                            des_loc, 
                                            depart_time, 
                                            mode_option) 

    instruction_dict = csr.build_instruction_dict(ori_loc, 
                                                  des_loc, 
                                                  depart_time, 
                                                  mode_option)

    enriched_route_dict = csr.enrich_routes_steps(google_route_dict)

    best_choice, google_route, enriched_route = csr.get_best_route(
                                                        loc_weight, 
                                                        google_route_dict,
                                                        enriched_route_dict)

    google_each_step_score = csr.get_each_step_score(loc_weight, 
                                                     google_route)

    enriched_each_step_score = csr.get_each_step_score(loc_weight, 
                                                       enriched_route)
    
    altered_route = csr.find_alternative_step(enriched_each_step_score, 
                                              depart_time, 
                                              mode_option,
                                              loc_weight)

    final_route = csr.get_route_for_map(google_route, 
                                        enriched_route, 
                                        altered_route)
    
    google_route_ls = csr.transfer_tuple_to_list(google_route)
    enriched_route_ls = csr.transfer_tuple_to_list(enriched_route)
    altered_route_ls = csr.transfer_tuple_to_list(altered_route)
    final_route_ls = csr.transfer_tuple_to_list(final_route)


    # For the purpose of debugging, printing the resultsN
    print()
    print('google_route_dict')
    print(google_route_dict)
    print()
    print('The safest route returned by Google API:')
    print(best_choice)
    print()
    print('enriched_each_step_score')
    print(enriched_each_step_score)
    print()
    print("google_route", len(google_route))
    print(google_route)
    print()
    print("google_route_ls", len(google_route_ls))
    print(google_route_ls)
    print()
    print("enriched_route", len(enriched_route))
    print(enriched_route)
    print()
    print("enriched_route_ls", len(enriched_route_ls))
    print(enriched_route_ls)
    print()
    print("altered_route", len(altered_route))
    print(altered_route)
    print()
    print("altered_route_ls", len(altered_route_ls))
    print(altered_route_ls)
    print()
    print("final_route", len(final_route))
    print(final_route)
    print()
    print("final_route_ls", len(final_route_ls))
    print(final_route_ls)
    print()
