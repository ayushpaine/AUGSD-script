# -*- coding: utf-8 -*-
"""AUGSD_prereq.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BveKohNNbVrT2PPLjwQJFyBQsqorWp4o
"""

# Import Required Libraries
import pandas as pd
import numpy as np

# Loading Required files into Pandas Dataframe

regdata = pd.read_csv("regdata.csv")
prereq = pd.read_excel("Pre-requisite_final.xlsx", skiprows = [0])

# prereq_data = pd.read_excel('/content/drive/MyDrive/Clubs/AUGSD/Pre-requisite_final.xlsx', skiprows = [0])    # Loading Pre-requisites file
# regdata = pd.read_csv('/content/drive/MyDrive/Clubs/AUGSD/regdata.csv')                                       # Loading Registration Data
prereq_data=prereq_data.rename(columns={'Unnamed: 10' : 'AO1','Unnamed: 16' : 'AO2','Unnamed: 22' : 'AO3',})  # Renaming AND/OR columns

# removing extra white spaces from input Data
regdata["Catalog"] = regdata["Catalog"].apply(lambda x : x.strip())
regdata["Subject"] = regdata["Subject"].apply(lambda x : x.strip())

cols = prereq_data.select_dtypes(['object']).columns
prereq_data[cols] = prereq_data[cols].apply(lambda x: x.str.strip())

# Loading Pre-requisite Subjects with their catalog code
preq1_sub = prereq_data.columns.get_loc("preq1 subject") 
preq1_cat = prereq_data.columns.get_loc("preq1 catalog") 
preq_ao1  = prereq_data.columns.get_loc("AO1")

preq2_sub = prereq_data.columns.get_loc("preq2 subject") 
preq2_cat = prereq_data.columns.get_loc("preq2 catalog") 
preq_ao2  = prereq_data.columns.get_loc("AO2")

preq3_sub = prereq_data.columns.get_loc("preq3 subject") 
preq3_cat = prereq_data.columns.get_loc("preq3 catalog") 
preq_ao3  = prereq_data.columns.get_loc("AO3")

preq4_sub = prereq_data.columns.get_loc("preq4 subject") 
preq4_cat = prereq_data.columns.get_loc("preq4 catalog") 

course_title = prereq_data.columns.get_loc("Title")

df_prereq = prereq_data.copy()        # making a copy of Pre-Requisite Data
df_prereq = df_prereq.to_numpy()      # converting the copied data to numpy
df_prereq = df_prereq.astype(str)     # changing the datatype of the data to string

idno = ""                 # 11 digit ID number
id_sub = {}               # Dictionary with ID numbers as keys and list of courses as values
id_studname = {}          # Dictionary with ID numbers as keys and Student Names as values
id_campusid = {}          # Dictionary with ID numbers as keys and Campus ID as values

# Code to get the list of courses taken by each student from the registration data

for row in regdata.itertuples() :
    if row.ID != idno :
        idno = row.ID
        id_sub[idno]=[]
        id_campusid[idno]=[]
        id_studname[idno]=[]
        id_sub[idno].append((row.Subject).strip() + ' ' +(row.Catalog).strip())
        id_studname[idno].append((row.Name))
        id_campusid[idno].append(row[regdata.columns.get_loc('ID')])
        
    else :
        if idno in id_sub :
            id_sub[idno].append((row.Subject).strip() + ' ' +(row.Catalog).strip()) 
            id_studname[idno].append((row.Name))
            id_campusid[idno].append(row[regdata.columns.get_loc('ID')])
            
            id_sub[idno] = list(set(id_sub[idno]))
            id_studname[idno] = list(set(id_studname[idno]))
            id_campusid[idno] = list(set(id_campusid[idno]))

print(id_sub)

# function to convert items of a list to a string
def alist(prereq_list):
    if(len(prereq_list) == 0):
        return '-'
    elif(len(prereq_list) > 0):

        return ' '.join(prereq_list)

#Getting index series from pre-requisite data
index = prereq_data.index                         

# Creating a new dataframe to display final results
final_df = pd.DataFrame(columns = ['Student Name', 'ID No.','BITS ID', 'Course Code', 'Course Title','Pre-requisites','Pre-Req Met', 'Comments'])

# The main Code - Pre-Requisite Check
for key, value in id_sub.items() :
    for i in value :  
        # initialising a list to store all Pre-Requisite courses
        prereq = []

        # Getting Subject and its code
        code = i[len(i) - 4 : len(i)]
        subject = i[0 : len(i) - 5]

        # initialising a bool series to tag the pre-requisite courses by using index
        condition = (prereq_data['Subject'] == subject) & (prereq_data['Catalog'] == code)
        
        # storing the index of pre-requisite course(s) and converting it to a python list
        indices = index[condition]
        indices_list = indices.tolist()
        
        # If course is not found
        if(len(indices_list) == 0) :
            final_df = final_df.append({'Course Title': 'NOT AVAILABLE','BITS ID': list(id_campusid[key])[0], 'Student Name': list(id_studname[key])[0],'ID No.': key, 'Course Code': subject + " " + code,'Pre-requisites': alist(prereq), 'Comments': 'Course not available','Pre-Req Met':'NA'},ignore_index = True)
 
        else:
            # getting the row number of the course
            course_row = indices_list[0]

            # Obtaining Course name using row number
            course_name = df_prereq[course_row][course_title]

            # Making a List of Pre-Requisite Courses along with AND/OR
            prereq.append(df_prereq[course_row][preq1_sub] + ' ' + df_prereq[course_row][preq1_cat]) 
            prereq.append(df_prereq[course_row][preq_ao1] ) 
            prereq.append(df_prereq[course_row][preq2_sub] + ' ' + df_prereq[course_row][preq2_cat]) 
            prereq.append(df_prereq[course_row][preq_ao2] )
            prereq.append(df_prereq[course_row][preq3_sub] + ' ' + df_prereq[course_row][preq3_cat]) 
            prereq.append(df_prereq[course_row][preq_ao3] )
            prereq.append(df_prereq[course_row][preq4_sub] + ' ' + df_prereq[course_row][preq4_cat])

            # Removing the Blank(nan) entries from the prereq list
            prereq = [x for x in prereq if(str(x) not in ['nan nan nan', 'nan nan', 'nan'])]
            
            # No Pre-Requisite Condition
            if (len(prereq) == 0) :
                final_df = final_df.append({'Course Title': course_name,'BITS ID': list(id_campusid[key])[0], 'Student Name': list(id_studname[key])[0], "ID No.": key, "Course Code": subject + " " + code,"Pre-requisites": alist(prereq) , "Comments": "No pre-requisites required", 'Pre-Req Met':'NA'},ignore_index = True)
            else : #Pre-Requisites Exist

                # Using a Flag system to detect Pre-Requiste Courses
                flag=0
                err1=0
                comments=[]
                skip_flag=0
                for ind,x in enumerate(prereq):
                    if skip_flag !=0:
                        skip_flag-=1
                        continue
                    if x in ['OR']:
                        flag=0
                        comments.append('and')
                        continue
                    elif x in ['AND']:
                        continue
                    else:
                        if flag == 0:
                            if x in value:
                                flag=0
                                if ind == len(prereq):
                                    if prereq[ind+1] in ['OR']:
                                        skip_flag=2
                            else:
                                flag=1
                                comments.append(x)
                        else:
                            err1=1
                            break

                if flag !=1: # All Pre-Requisites Met Condition
                    final_df = final_df.append({'Course Title': course_name,'BITS ID': list(id_campusid[key])[0], 'Student Name': list(id_studname[key])[0], "ID No.": key, "Course Code": subject + " " + code,"Pre-requisites": alist(prereq), "Comments": "Pre-requisites met", 'Pre-Req Met': '1'},ignore_index = True)
                else: # Pre-Requisites NOT Met Condition
                    final_df = final_df.append({'Course Title': course_name,'BITS ID': list(id_campusid[key])[0], 'Student Name': list(id_studname[key])[0], "ID No.": key, "Course Code": subject + " " + code,"Pre-requisites": alist(prereq), "Comments": "Pre-requisites " + ' '.join(comments) + " not met", 'Pre-Req Met': '0'},ignore_index = True)

final_df

# Code to detect if a Course has a Pre-Requisite course being taken for which the Pre-Requisites are not satisfied

# iterating through the dataframe final_df
for i,row in final_df.iterrows():

    # Checking for courses which are tagged as Pre-Requisites Met
    if str(getattr(row,'Pre-Req Met')) == '1':

        # Storing ID number
        id_req=getattr(row,'ID No.')                                            

        # Getting Pre-Requisite courses
        req = list(map(str.strip,getattr(row,'Pre-requisites').split('AND')))
        if len(req)==1:
            req = list(map(str.strip, getattr(row,'Pre-requisites').split('OR')))
        
        # Iterating through Pre-Requisite courses. #
        for data in req:
            # Searching for courses taken by using ID number and course code and checking if Pre-Requisites are Met
            temp=final_df.loc[(final_df['ID No.'] == id_req) & (final_df['Course Code'] == data), ['Pre-Req Met']]

            # Taking the bool value of Pre-Requisites Met condition
            temp=" ".join(temp['Pre-Req Met'].values)

            # Checking if Pre-Requisites are met (bool value check)
            if str(temp) == '0':
                # Changing Pre-Req Met Tag to 0 as Pre-Requisites not met
                final_df.at[i,'Pre-Req Met'] = 0

                # Changing Comments as Pre-Requisites not met
                final_df.at[i,'Comments'] = 'Pre-Requisites of ' + data + ' not met'
               
final_df

prereq

