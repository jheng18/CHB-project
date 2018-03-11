# CS122 project
# CHB Group
## Xi Chen, Jie Heng, Chen Bao


### Each member' role and codes:

####  Data: Chen Bao



####  Algorithm: Xi Chen
   
   The codes are in the "route" folder, including
   
   Compute_crime_weights.py
   
   Subset_date_by_time.py
   
   Choose_safest_route.py
   
   Get_route_for_map.py
   

#### Website: Jie Heng







### An sample run for the the Algorithm codes:

1. Create a folder called "route", save the four algorithm's python files in this folder; Then, create a folder called "Data" inside the "route" folder, put the "final_data.csv" into this "Data" folder.

2. In the VM, go to the directory ".../route", run the following two commands:
   
   python Compute_crime_weights.py
   
   python Subset_date_by_time.py
   
   The second command takes about 15 seconds. After executing these two commands, in the "Data" folder, twenty-five new csv files will be created: one is called "data_with_weight.csv", and the other are the subsets of the crime data according to twenty-four hours.

3. In the VM, install the google map package by running the following commands:

   sudo pip3 install -U googlemaps
   
4. In the "Get_route_for_map.py" python file, between line 17-22, there is an example of user' inputs. Run the following command:

   python Get_route_for_map.py
   
   There are several outputs which show different versions of the route in the process of the algorithm. You can change the user's inputs to have another sample test. There is one important thing that needs be kept in mind, when entering the departure date and time, the user has to enter an future date and time, or at least the current date/time, because the Google Map API would only accept the future or at least current date and time. 
   
   
