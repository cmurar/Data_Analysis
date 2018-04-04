
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import heapq as h
import matplotlib.pyplot as plt
import csv
import datetime

# Reading the csv. file and getting a list of all the data in the file
f = open("guns.csv","r")
data = list(csv.reader(f))
headers = data[1:] # removing the headers

#extracting year column from data
years = [i[1] for i in data]
#check how many gun death occured each year and store the information in the years_count dict
years_counts = {}
for j in years:
    if j in years_counts:
        years_counts[j] +=1
    else:
        years_counts[j] = 1
        
#check if the gun deatch rate has changed on monthly level and similar as above store the information in a dict 
dates = []
dates = [datetime.datetime(year = int(i[1]), month = int(i[2]) , day=1 ) for i in headers] 
date_counts = {}
for j in dates:
    if j in date_counts:
        date_counts[j] +=1
    else:
        date_counts[j] =1


gender_counts = {}
race_counts = {}
#count how many times each item occures in Gender column
for i in headers:
    name = i[5]
    if name in gender_counts:
        gender_counts[name] +=1
    else:
        gender_counts[name] =1
#count how many times each item occures in Race column
for r in headers:
    race = r[7]
    if race in race_counts:
        race_counts[race] +=1
    else:
        race_counts[race] =1

intents = [i[3] for i in data] #extracting Intent column into a list
races = [i[7] for i in data] # extracting Race column into a list
homicide_race_counts = {}
#loop through each item of races list and check if the value at position 'i' in intents list equals to 'Homicide'
for i,race in enumerate(races):
    if intents[i] == 'Homicide':
        if race in homicide_race_counts:
            homicide_race_counts[race] +=1
        else:
            homicide_race_counts[race] = 1
            
# create a dictionary that maps each key from race_counts or homicide_race_counts to the population count of race from census.csv
mapping = {}
def race_list(x):
    f = open("census.csv","r")
    census = list(csv.reader(f))
    census = census [1:]
    for key,value in x.items():
        if key == 'Asian/Pacific Islander':
            for i in census:
                counts_asian = int(i[14]) + int(i[15])
            mapping[key] = counts_asian
        else:
            if key == 'Black':
                for i in census:
                    counts_black = int(i[12])
                mapping[key] = counts_black
            else:
                if key == 'Hispanic':
                    for i in census:
                        counts_hispanic = int(i[11])
                    mapping[key] = counts_hispanic
                else:
                    if key == 'Native American/Native Alaskan':
                        for i in census:
                            counts_native = int(i[13])
                        mapping[key] = counts_native
                    else:
                        if key == 'White':
                            for i in census:
                                counts_white = int(i[10])
                            mapping[key] = counts_white  
    return mapping

mapping_race = race_list(race_counts) #calling the function above for race_counts
mapping_homicide = race_list(homicide_race_counts) #calling the function above for homicide_race_counts
#Calculate rates to 100.000 people
#Create empty dict and loop through each key of race_counts by the value associated with the key in mapping
race_per_hundredk = {}
for i,j in race_counts.items():
    for m,n in mapping_race.items():
        if i == m:
            race_per_hundredk[m] = round(j*100000/n)
print("Proportion #gundeaths: ")
print(race_per_hundredk)
race_homicide_per_hundredk = {}
for i,j in homicide_race_counts.items():
    for m,n in mapping_homicide.items():
        if i == m:
            race_homicide_per_hundredk[m] = round(j*100000/n)
print("Proportion #gundeaths with homicide intent: ")
print(race_homicide_per_hundredk)

#reading the file and storing the data in a dataframe
f_read = pd.read_csv("guns.csv")
df = pd.DataFrame(f_read, columns = ['month','intent','sex','place','education'])
df_hom = df[df['intent'].str.contains('Homicide',na = False)] #creating a df filtered for 'Homicide' intent

homucide_count_month = df_hom[["month","intent"]].groupby('month').agg({'intent':'count'})
homucide_count_gender = df_hom[["sex","intent"]].groupby('sex').agg({'intent':'count'})
death_count_location = df[["place","intent"]].groupby('place').agg({'intent':'count'})
death_count_edu = df[["education","intent"]].groupby('education').agg({'intent':'count'})
#plotting the graphs
homucide_count_gender.plot.bar()
plt.title('#homicide deaths per Gender')
homucide_count_month.plot.line()
plt.title('#homicide deaths per Month')
death_count_edu.plot.bar()
plt.title('#gun deaths per Education')
death_count_location.plot(kind='bar',alpha=0.75, rot=90)
plt.xlabel("")
plt.title('#gun deaths per Location')
plt.show()
        

