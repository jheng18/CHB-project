# CS122 project
# CHB Group

## Xi Chen, Jie Heng, Chen Bao


###  01 Data Prep and Visualization: Chen Bao 

Data prep and visualization folder contains files including:

Crimes_2001_to_present.scv
      This is the original CSV file we downloaded from City of Chicago Data Portal (last updated on Feb 20th), dataset reflects reported        incidents of crime (with the exception of murders where data exists for each victim) that occurred in the City of Chicago from 2001 to present

Modify_csv_data.py 
      Read in the original data file and format the data for future use

Get_Security_Alert.py 
      Crawl data from University of Chicago security alerts archive

FBI_Code.py
      Crawl data from Chicago Police Department Clear Map Crime Summary 

Merge_two_dataset.py 
      Merge data output from Modify_csv_data.py and Get_Security_Alert.py 

Convert_to_dict.py
      Convert the output from Modify_csv_data.py into a dictionary and export as json file

Data_viz.py 
      Use Python Seaborn package to create data visualizations and perform data analysis 



###  02 Algorithm: Xi Chen
   
   In the "02 Algorithm" folder, there are four python codes:
   
   Compute_crime_weights.py
   
   Subset_date_by_time.py
   
   Choose_safest_route.py
   
   Get_route_for_map.py
  
#### An sample run for the the Algorithm codes:

1. Download the four python codes above from the "02 Algorithm" folder, and download the "final_data.csv" from the "Data" folder inside the "02 Algorithm" folder.

2. In your computer, create a folder called "Algorithm", save the four algorithm's python files in this folder; inside the "Algorithm" folder, create a folder called "Data", save the "final_data.csv" in this folder.

3. In the VM, go to the directory "./Algorithm", run the following two commands:
   
   python Compute_crime_weights.py
   
   python Subset_date_by_time.py
   
   The second command takes about 45 seconds. After executing these two commands, in the "Data" folder, twenty-five new csv files will be created: one is called "data_with_weight.csv", and the other are the subsets of the crime data according to twenty-four hours.

3. In the VM, install the google map package by running the following commands:

   sudo pip3 install -U googlemaps
   
4. In the "Get_route_for_map.py" python file, between line 17-22, there is an example of user' inputs. Run the following command:

   python Get_route_for_map.py
   
   There are several outputs which show different versions of the route in the process of the algorithm. You can change the user's inputs to have another sample test. There is one important thing that needs be kept in mind, when entering the departure date and time, the user has to enter an future date and time, or at least the current date/time, because the Google Map API would only accept the future or at least current date and time. 
   
   
   
### Website: Jie Heng
