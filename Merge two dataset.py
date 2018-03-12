import pandas as pd
hyde_park = pd.read_csv('Hyde_park_crime.csv')
security_alert_df = pd.read_csv('Security Alert Data.csv')

# security_alert_df.set_index(['Date', 'PrimaryType'], inplace=True)
# hyde_park.set_index(['Date', 'PrimaryType'], inplace=True)
#
# hyde_park.join(security_alert_df).reset_index()

security_alert_df = security_alert_df.apply(lambda x: x.astype(str).str.upper())

data_filter = (security_alert_df.Location != "NAN") & (security_alert_df.Time != "NAN") & (security_alert_df.PrimaryType != "CRIMINAL TRESPASS")
security_alert_df = security_alert_df[data_filter]

security_alert_df['Latitude'] = security_alert_df['Location'].str[1:10]
security_alert_df['Longitude'] = security_alert_df['Location'].str[12:22]

security_alert_df['Time'] = security_alert_df['Time'].map(lambda x: str(x)[:-2])

final_df = hyde_park.append(security_alert_df, ignore_index=True)

final_df["Date"] = final_df["Date"].astype(int)
final_df = final_df.rename(index=str, columns={"FBI Code": "FBI"})

list = final_df.FBI.unique()

Crime_Type = {'OTHER OFFENSE':  'Crime Against Society',
              'LIQUOR LAW VIOLATION': 'Crimes Against Society' ,
              'DECEPTIVE PRACTICE': 'Crimes Against Property' ,
              'INTERFERENCE WITH PUBLIC OFFICER': 'Crime Against Society',
              'PUBLIC PEACE VIOLATION': 'Crime Against Society',
              'CONCEALED CARRY LICENSE VIOLATION': 'Crime Against Society' ,
              'NARCOTICS': 'Crime Against Society',
              'THEFT': 'Crimes Against Property' ,
              'STALKING': 'Crimes Against Persons',
              'INTIMIDATION': 'Crime Against Society',
              'CRIMINAL DAMAGE': 'Crime Against Property' ,
              'OBSCENITY': 'Crimes Against Persons and Society',
              'PUBLIC INDECENCY': 'Crimes Against Persons and Society',
              'MOTOR VEHICLE THEFT': 'Crime Against Property' ,
              'BURGLARY': 'Crime Against Property',
              'ROBBERY': 'Crime Against Property',
              'ASSAULT': 'Crimes Against Persons',
              'BATTERY': 'Crimes Against Persons',
              'WEAPONS VIOLATION':'Crimes Against Society',
              'KIDNAPPING': 'Crime Against Society',
              'CRIM SEXUAL ASSAULT': 'Crimes Against Persons',
              'SEX OFFENSE': 'Crimes Against Persons and Society',
              'OFFENSE INVOLVING CHILDREN': 'Crimes Against Persons',
              'HOMICIDE': 'Crimes Against Persons',
              'HUMAN TRAFFICKING': 'Crimes Against Persons and Society',
              'MURDER': 'Crimes Against Persons' }
final_df['CrimeType'] = final_df['PrimaryType'].map(Crime_Type)

import operator
Crime_Type = {'OTHER OFFENSE':  300,
              'LIQUOR LAW VIOLATION': 300,
              'WEAPONS VIOLATION': 300,
              'KIDNAPPING': 300,
              'INTERFERENCE WITH PUBLIC OFFICER': 300,
              'PUBLIC PEACE VIOLATION': 300,
              'CONCEALED CARRY LICENSE VIOLATION': 300,
              'NARCOTICS': 300,
              'INTIMIDATION': 300,
              'THEFT': 200,
              'MOTOR VEHICLE THEFT': 200,
              'BURGLARY': 200,
              'ROBBERY': 200,
              'DECEPTIVE PRACTICE': 200,
              'CRIMINAL DAMAGE': 200,
              'OBSCENITY': 500,
              'SEX OFFENSE': 500,
              'PUBLIC INDECENCY': 500,
              'HUMAN TRAFFICKING': 500,
              'STALKING': 400,
              'ASSAULT': 400,
              'BATTERY': 400,
              'CRIM SEXUAL ASSAULT': 400,
              'OFFENSE INVOLVING CHILDREN': 400,
              'HOMICIDE': 400,
              'MURDER': 400}

#sorted_x = sorted(Crime_Type.items(), key=lambda x: x[1])
final_df.to_csv("Final_data_all_columns.csv", index = False)





useful_col = ['Date', 'Time', 'PrimaryType', 'Latitude', 'Longitude', 'Location']
final_df = final_df[useful_col]

final_df = final_df.sort_values(by=['Date', 'Time'], ascending=True)

final_df.to_csv("Final_data.csv", index = False)

