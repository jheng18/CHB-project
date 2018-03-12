import pandas as pd
import json

# import hyde_park_crime data into pandas data frame
hyde_park = pd.read_csv('Hyde_park_crime.csv')
hyde_park = hyde_park.rename(index=str, columns={"Unnamed: 0": "Index"})

# make the new columns using string indexing
hyde_park['Date'] = hyde_park['Date'].astype(str).str[4:8]
hyde_park['Date'] = hyde_park['Date'].astype(int)

# filter out years that are not useful
hyde_park = hyde_park[(hyde_park.Year == 2017)]


hyde_park['Date'] = hyde_park['Date'].astype(str)
# make all upper case in to lower case
hyde_park = hyde_park.apply(lambda x: x.astype(str).str.lower())

# convert columns into float
hyde_park['Latitude'] = hyde_park['Latitude'].astype(float)
hyde_park['Longitude'] = hyde_park['Longitude'].astype(float)

# convert data frame columns into list
ID = hyde_park["ID"].tolist()
PrimaryType = hyde_park["PrimaryType"].tolist()
Latitude = hyde_park["Latitude"].tolist()
Longitude = hyde_park["Longitude"].tolist()
X_Coordinate = hyde_park["X Coordinate"].tolist()
Y_Coordinate = hyde_park["Y Coordinate"].tolist()
# define a dictionary
hyde_park_list = []

for i in range(len(ID)):
    i = {"type": PrimaryType[i],"geometry": {"type": "Point", "location": (X_Coordinate[i], Y_Coordinate[i])}}
                         #"properties": {"year": Year[i], "date": Date[i], "time": Time[i]},
                         #"geometry": {"type": "point", "location": (Latitude[i], Longitude[i])},
                         #"id": ID[i]}
    hyde_park_list.append(i)

final_dict = {}
final_dict = {"features": hyde_park_list}

# drop dictionary key
if 'key' in final_dict:
    del final_dict['key']

# export as a json file
with open('final_dict.json', 'w') as fd:
    json.dump(final_dict, fd)

