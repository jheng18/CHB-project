import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar

sns.set()

# import data into pandas data frame
crime_df = pd.read_csv('Final_data_all_columns.csv')

# take out the month data from thr date data
crime_df['Month'] = crime_df['Date'].map(lambda x: str(x)[4:6])

# filter out if year == 2018
crime_df = crime_df[(crime_df.Year < 2018)]

# convert Year, Month, and Time string into int
crime_df["Year"] = crime_df["Year"].astype(int)
crime_df["Month"] = crime_df["Month"].astype(int)
crime_df["Time"] = crime_df["Time"].astype(int)

# create a list for month
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#check_frequency = crime_df.groupby(["PrimaryType"])["ID"].count().reset_index(name="count").sort_values("count")

# Categorize crime type into five bigger type
Crime_Type = {'OTHER OFFENSE':'Crime Against Society',
              'LIQUOR LAW VIOLATION':'Crime Against Society',
              'DECEPTIVE PRACTICE':'Crime Against Property',
              'INTERFERENCE WITH PUBLIC OFFICER':'Crime Against Society',
              'PUBLIC PEACE VIOLATION':'Crime Against Society',
              'CONCEALED CARRY LICENSE VIOLATION': 'Crime Against Society',
              'NARCOTICS': 'Crime Against Society',
              'THEFT': 'Crime Against Property',
              'STALKING': 'Crime Against Persons',
              'INTIMIDATION': 'Crime Against Society',
              'CRIMINAL DAMAGE': 'Crime Against Property',
              'OBSCENITY': 'Crime Against Persons and Society',
              'PUBLIC INDECENCY': 'Crime Against Persons and Society',
              'MOTOR VEHICLE THEFT': 'Crime Against Property',
              'BURGLARY': 'Crime Against Property',
              'ROBBERY': 'Crime Against Property',
              'ASSAULT': 'Crime Against Persons',
              'BATTERY': 'Crime Against Persons',
              'WEAPONS VIOLATION':'Crime Against Society',
              'KIDNAPPING': 'Crime Against Society',
              'CRIM SEXUAL ASSAULT': 'Crime Against Persons',
              'SEX OFFENSE': 'Crime Against Persons and Society',
              'OFFENSE INVOLVING CHILDREN': 'Crime Against Persons',
              'HOMICIDE': 'Crime Against Persons',
              'HUMAN TRAFFICKING': 'Crime Against Persons and Society',
              'MURDER': 'Crime Against Persons'}
crime_df['CrimeType'] = crime_df['PrimaryType'].map(Crime_Type)
# Rename crime type
Crime_Acronym = {'OTHER OFFENSE':'Offense etc.',
              'LIQUOR LAW VIOLATION': 'Liquor Vio',
              'DECEPTIVE PRACTICE': 'Deceit',
              'INTERFERENCE WITH PUBLIC OFFICER': 'Interference',
              'PUBLIC PEACE VIOLATION': 'Peace Vio',
              'CONCEALED CARRY LICENSE VIOLATION': 'License Vio',
              'NARCOTICS': 'Narcotics',
              'THEFT': 'Theft',
              'STALKING': 'Stalking',
              'INTIMIDATION': 'Intimidation',
              'CRIMINAL DAMAGE': 'Damage',
              'OBSCENITY': 'Obscenity',
              'PUBLIC INDECENCY': 'Indecency',
              'MOTOR VEHICLE THEFT': 'Motor Theft',
              'BURGLARY': 'Burglary',
              'ROBBERY': 'Robbery',
              'ASSAULT': 'Assault',
              'BATTERY': 'Battery',
              'WEAPONS VIOLATION': 'Weapon Vio',
              'KIDNAPPING': 'Kidnapping',
              'CRIM SEXUAL ASSAULT': 'Sexual Vio',
              'SEX OFFENSE': 'Sex Offense',
              'OFFENSE INVOLVING CHILDREN': 'Child Abuse',
              'HOMICIDE': 'Homicide',
              'HUMAN TRAFFICKING': 'Human Traffic',
              'MURDER': 'Murder'}
crime_df['CrimeAcronym'] = crime_df['PrimaryType'].map(Crime_Acronym)

# group by function
def group_by(dataframe, column1, column2, column3):
    new = dataframe.groupby([column1, column2])[column3].count().reset_index(name="count")
    return new

# sort column values function
def sort_values(dataframe, column):
    new = dataframe.sort_values(column)
    return new

def pivot(dataframe, column1, column2, column3):
    new = dataframe.pivot(column1, column2, column3)
    return new

def fillna(dataframe):
    new = dataframe.fillna(0)
    return new

def astype_int(dataframe):
    new = dataframe.astype(int)
    return new

# figure 1 -- month and year overall
def crime1():
    crime_1 = group_by(crime_df, "Year", "Month", "ID")
    crime_1 = sort_values(crime_1, "Month")
    crime_1['Month'] = crime_1['Month'].apply(lambda x: calendar.month_abbr[x])
    crime_1 = pivot(crime_1, "Year", "Month", "count")
    crime_1 = crime_1[month_list]
    return crime_1

def heat_map_1(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    ax.invert_yaxis()
    map.set_title('Count for Crime by Month, 2013 - 2017', fontsize=20)
    map.figure.savefig("Count for Crime by Month, 2013 - 2017.png")

figure_1 = heat_map_1(crime1())


# figure 2 -- primary crime type and year overall
def crime_2():
    crime_2 = group_by(crime_df, "Year", "CrimeAcronym", "ID")
    crime_2 = pivot(crime_2, "Year", "CrimeAcronym", "count")
    crime_2 = fillna(crime_2)
    crime_2 = astype_int(crime_2)
    crime_2 = crime_2.reindex(sorted(crime_2.columns, key=lambda x: crime_2[x][2017]), axis=1)
    cols = (crime_2 >= 2).any()
    crime_2 = crime_2[cols[cols].index]
    return crime_2

def heat_map_2(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    sns.set(font_scale=0.7)
    ax.invert_yaxis()
    map.set_title('Count for Crime by Primary Crime Type, 2013 - 2017',fontsize=20)
    map.figure.savefig("Count for Crime by Primary Crime Type, 2013 - 2017.png")

figure_2 = heat_map_2(crime_2())


# figure 3 -- aggregate crime type and year overall
crime_3 = crime_df.groupby(["Year", "CrimeType"])["ID"].count().reset_index(name="count")
crime_3 = crime_3.pivot("Year", "CrimeType", "count")
crime_3 = crime_3.fillna(0)
crime_3 = crime_3.astype(int)

def heat_map_3(dataframe):
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(dataframe, annot=True, fmt="d", linewidths=.5, ax=ax, cmap="YlOrRd")
    ax.invert_yaxis()
    map.set_title('Count for Crime by Aggregate Crime Type, 2013 - 2017',fontsize=20)
    map.figure.savefig("Count for Crime by Aggregate Crime Type, 2013 - 2017.png")

figure_3 = heat_map_3(crime_3)


# Graph 4 -- each year and am/pm
def time_slot (row):
    if 000 <= row['Time'] < 200:
        return '0am-2am'
    if 200 <= row['Time'] < 400:
        return '2am-4am'
    if 400 <= row['Time'] < 600:
        return '4am-6am'
    if 600 <= row['Time'] < 800:
        return '6am-8am'
    if 800 <= row['Time'] < 1000:
        return '8am-10am'
    if 1000 <= row['Time'] < 1200:
        return '10am-12pm'
    if 1200 <= row['Time'] < 1400:
        return '12pm-2pm'
    if 1400 <= row['Time'] < 1600:
        return '2pm-4pm'
    if 1600 <= row['Time'] < 1800:
        return '4pm-6pm'
    if 1800 <= row['Time'] < 2000:
        return '6pm-8pm'
    if 2000 <= row['Time'] < 2200:
        return '8pm-10pm'
    if 2200 <= row['Time'] < 2400:
        return '10pm-12am'
    if row['Time'] >= 2400:
        return '12pm-2pm'

crime_df.apply (lambda row: time_slot (row),axis=1)
crime_df['Time Slot'] = crime_df.apply (lambda row: time_slot (row), axis=1)

crime_df_am_pm = crime_df.sort_values('Time')


def histogram_1(column, dataframe):
    hist = sns.factorplot(x=column, data=dataframe, kind="count",
                       palette="BuPu", size=6, aspect=1.5)
    sns.set(font_scale=1)
    hist.set_xticklabels(step=2)
    plt.subplots_adjust(top=0.9)
    hist.fig.suptitle('Count for Crime by Time Slot, 2013 - 2017', fontsize=20)
    hist.savefig("Count for Crime by Time Slot, 2013 - 2017.png")

figure_4 = histogram_1("Time Slot", crime_df_am_pm)

# sub figure 2 -- primary crime type by month, year
def primary_crime_type_by_month(year):
    crime_df_by_year = crime_df[(crime_df.Year == year)]
    crime_df_by_year = crime_df_by_year.groupby(["Month", "CrimeAcronym"])["ID"].count().reset_index(name="count")
    crime_df_by_year['Month'] = crime_df_by_year['Month'].apply(lambda x: calendar.month_abbr[x])
    crime_df_by_year = crime_df_by_year.pivot("CrimeAcronym", "Month", "count")
    crime_df_by_year = crime_df_by_year.fillna(0)
    crime_df_by_year = crime_df_by_year.astype(int)
    crime_df_by_year = crime_df_by_year[month_list]
    cols = (crime_df_by_year >= 2).any()
    crime_df_by_year = crime_df_by_year[cols[cols].index]
    return crime_df_by_year


def primary_crime_type_2013():
    pct_2013 = primary_crime_type_by_month(2013)
    f, ax = plt.subplots(figsize=(9, 6))
    map = sns.heatmap(pct_2013, annot=True, fmt="d", linewidths=.5, ax=ax)
    ax.invert_yaxis()
    map.set_title('Count for Crime, by Primary Crime Type and by Month', fontsize=20)
    map.figure.savefig("Count for Crime, by Year and Aggregate Crime Type.png")

pct_2014 = primary_crime_type_by_month(2014)
pct_2015 = primary_crime_type_by_month(2015)
pct_2016 = primary_crime_type_by_month(2016)
pct_2017 = primary_crime_type_by_month(2017)








g = sns.factorplot(x="Time Slot", data=crime_df_am_pm, kind="count",
                   palette="BuPu", size=6, aspect=1.5)
g.set_xticklabels(step=2)

def crime_hist_by_year(year):
    crime_df_am_pm_year = crime_df_am_pm[(crime_df_am_pm.Year == year)]
    g = sns.factorplot(x="TimeSlot", data=crime_df_am_pm_year, kind="count",
                       palette="BuPu", size=6, aspect=1.5)
    g.set_xticklabels(step=2)
    g.set_titles("histgram")

hist_by_year_2013 = crime_hist_by_year(2013)
hist_by_year_2014 = crime_hist_by_year(2014)
hist_by_year_2015 = crime_hist_by_year(2015)
hist_by_year_2016 = crime_hist_by_year(2016)
hist_by_year_2017 = crime_hist_by_year(2017)


g = sns.factorplot(x="CrimeType", data=crime_df_am_pm, kind="count",
                   palette="BuPu", size=6, aspect=1.5)
g.set_xticklabels(step=2)

def crime_hist_crimetype_by_year(year):
    crime_df_am_pm_year = crime_df_am_pm[(crime_df_am_pm.Year == year)]
    g = sns.factorplot(x="CrimeType", data=crime_df_am_pm_year, kind="count",
                       palette="BuPu", size=6, aspect=1.5)
    g.set_xticklabels(step=2)
    g.set_titles("histgram")

hist_by_year_crimetype_2013 = crime_hist_crimetype_by_year(2013)
hist_by_year_crimetype_2014 = crime_hist_crimetype_by_year(2014)
hist_by_year_crimetype_2015 = crime_hist_crimetype_by_year(2015)
hist_by_year_crimetype_2016 = crime_hist_crimetype_by_year(2016)
hist_by_year_crimetype_2017 = crime_hist_crimetype_by_year(2017)