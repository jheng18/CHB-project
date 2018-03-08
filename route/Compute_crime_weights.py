import csv
import pandas as pd
import numpy as np
import re
import string

# Assign different weights for various crime types
CRIME_TYPE = {'OTHER OFFENSE':100, 
              'LIQUOR LAW VIOLATION': 100, 
              'DECEPTIVE PRACTICE': 100,
              'INTERFERENCE WITH PUBLIC OFFICER': 100, 
              'PUBLIC PEACE VIOLATION': 100, 
              'CONCEALED CARRY LICENSE VIOLATION': 200, 
              'WEAPONS VIOLATION': 200,  
              'NARCOTICS': 200, 
              'THEFT': 200,
              'STALKING': 200,
              'INTIMIDATION': 300,
              'CRIMINAL DAMAGE': 300,
              'OBSCENITY': 300, 
              'PUBLIC INDECENCY': 300,
              'MOTOR VEHICLE THEFT': 300,
              'BURGLARY': 400,
              'CRIMINAL TRESPASS': 400,
              'ROBBERY': 400,
              'ASSAULT': 400,
              'BATTERY': 400,
              'KIDNAPPING': 500,
              'CRIM SEXUAL ASSAULT': 500,
              'SEX OFFENSE': 500,
              'OFFENSE INVOLVING CHILDREN': 500,
              'HOMICIDE': 500,
              'HUMAN TRAFFICKING': 500,
              'MURDER': 500
}


if __name__ == "__main__":

	# Read Crime data
	df = pd.read_csv('./Data/Final_data.csv')

	df['type_weight'] = df['PrimaryType'].map(CRIME_TYPE)

	# Assign different weights for various Crime Date
	date_num_dict = df.groupby(['Date']).size().to_dict()
	date_ls = [*date_num_dict]

	date_dist = {}
	i = 1
	for date in date_ls:
	    date_dist[date] = ((i / len(date_ls))**2) * 1000
	    i += 1

	df['date_weight'] = df['Date'].map(date_dist)

	# Compute the toal weight for each unique crime location
	df['weight'] = df.type_weight * df.date_weight
	df.to_csv('./Data/data_with_weight.csv', index=False)

