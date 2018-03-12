import pandas as pd


# import data into pandas data frame
crime_df = pd.read_csv('Crimes_-_2001_to_present.csv')
# remove all the white spaces in the column names
crime_df.columns = crime_df.columns.str.replace('\s+', '')

# create filter for hyde park longitude and latitude
latitude_filter = (crime_df.Latitude >= 41.78013) & (crime_df.Latitude <= 41.809241)
longitude_filter = (crime_df.Longitude >= -87.615546) & (crime_df.Longitude <= -87.575706)

# create filter for data crime year
year_filter = (crime_df.Year >= 2013)

# create filter for data crime type
def hyde_park_crime_all_years():
    temp = filter(crime_df, latitude_filter)
    temp = filter(temp, longitude_filter)
    temp.to_csv("hyde_park_crime_all_years.csv", index=False)
    return temp


def hyde_park_crime_after_2013():
    temp = hyde_park_crime_all_years()
    temp = filter(temp, year_filter)
    print(temp)
    return temp

def rename_column_name(dataframe, column, new_column):
    temp = dataframe.rename(index=str, columns={column: new_column})
    return temp

def filter(dataframe, filter):
    temp = dataframe[filter]
    return temp

def data_to_csv(dataframe, name):
    return dataframe.to_scv(name, index=False)


# crime_df = crime_df.rename(index=str, columns={"Primary Type": "PrimaryType"})
# crime_df = crime_df.rename(index=str, columns={"Date": "DateString"})

# crime_df = crime_df[latitude_filter]
# crime_df = crime_df[longitude_filter]


# Filter out years
#crime_df = crime_df[(crime_df.Year >= 2013)]

# filter out data by crime type
# Not include Arson, Criminal Trespass, Gambling, Prostitution, Ritualism
crime_filter = (crime_df.PrimaryType != "ARSON") & (crime_df.PrimaryType != "CRIMINAL TRESPASS") & \
                (crime_df.PrimaryType != "GAMBLING") & (crime_df.PrimaryType != "PROSTITUTION") & \
                (crime_df.PrimaryType != "RITUALISM")

crime_df = crime_df[crime_filter]
crime_df = crime_df.reset_index(drop=True)

# Spilt time column into Date, Time, and AM/PM
date_df = pd.DataFrame(crime_df.DateString.str.split(' ',2).tolist(),columns = ['Date','Time','AM/PM'])

# Transfer Date and Time strings into integers
def transfer_date_to_int(date_str):
    month, day, year = date_str.split('/')
    return int(year)*10000 + int(month)*100 + int(day)

def transfer_time_to_int(time_str):
    hour, minute, second = time_str.split(':')
    return int(hour) * 100 + int(float(minute)/60*100)

def transfer_date_time_type(time_df):
    for i in range(len(time_df)):
        date = transfer_date_to_int(time_df.Date[i])
        time_df.Date[i] = date

        time = transfer_time_to_int(time_df.Time[i])

        if time_df['AM/PM'][i] == 'PM':
            time_df.Time[i] = time + 1200
        else:
            time_df.Time[i] = time

    return time_df

adjusted_date_df = transfer_date_time_type(date_df)

for i in range(len(adjusted_date_df)):
    if adjusted_date_df["Time"][i] >= 2400:
        adjusted_date_df["Time"][i] = adjusted_date_df["Time"][i] - 1200
    if (1200 <= adjusted_date_df["Time"][i]) & (adjusted_date_df["Time"][i] <= 1300) & (adjusted_date_df["AM/PM"][i] == "AM"):
        adjusted_date_df["Time"][i] = adjusted_date_df["Time"][i] - 1200

# Join dataframes
final_crime_df = pd.concat([crime_df, adjusted_date_df], axis=1, join='inner')

# Export as CSV
final_crime_df.to_csv("Hyde_park_crime.csv", index = False)

if __name__ == "__main__":
    hyde_park_crime_all_years()

