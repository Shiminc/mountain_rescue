import pandas as pd
import json
import time
from datetime import timedelta, date, datetime 
import numpy as np
import altair as alt
import os 

PATH = "../../data/all_incidents.json"



def moving_averages(series, window):
    new_series = []
    for i in range(0, len(series)):
      if i < (window - 1):
          new_series.append(pd.NA)
      else:
          elms_in_window = []
          for j in range(0,window):
              elms_in_window.append(series[i-window+1+j])
          new_series.append(np.mean(elms_in_window))    

        #   element_in_window = [series[i - window + 1], series[i-wi]]      

    return new_series


def read_json_to_df(path):
    # load the json
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    
    # read into the df
    data_pd = pd.DataFrame(data)

    return data_pd

def format_time_columns(df):
    df['date'] = pd.to_datetime(df['date'], format='%d %b %Y')
    # df.sort_values(by=['date'])
    df['year'] = df['date'].dt.year.astype(int)
    df['month'] = df['date'].dt.month.astype(int)
    df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')

    return df

def filter_by_year(df,year):
    df = df[df['year']>year]
    return df


def aggregate_by_year_month(df, start_date='2015-01-01', end_date='2025-11-01', freq='MS'):
    #create a dummy series that include all date so that when we merge with the data, any month without any incident will be able to filled with 0
    index = pd.date_range(start_date, end_date, freq=freq)
    dummy_series = pd.Series(index=index,name='dummy')

    incident_count = df.pivot_table(index=['year_month'],
                              #columns='Incident_Type',
                              values='Incident',
                              aggfunc='count', 
                              fill_value=0)
                              #margins=True
    merged_df = pd.merge(dummy_series, incident_count, how = 'left', left_index=True, right_index=True)
    merged_df.drop(labels='dummy', axis='columns', inplace=True)
    merged_df.fillna(0,inplace=True)
    merged_df.reset_index(inplace=True)
    merged_df.columns=['dateTime','Incident']
    merged_df['year']=merged_df.dateTime.dt.year
    merged_df['month']=merged_df.dateTime.dt.month
    merged_df['year_month']= pd.to_datetime(merged_df['dateTime'], format = "%Y-%m-%d").astype(str)
    merged_df['moving_average']=moving_averages(merged_df.Incident,12)
    return merged_df

def handling_problematic_data(data):
    # empty cell in incident cause to be recoded to another original value Other
    # data.Incident_Cause[data.Incident_Cause=='']='Other'
    # data['Incident_Cause'].replace({'': 'Other'})
    # other could include help sweeping snow or flood or dog https://www.wmrt.org.uk/incidents/corney-fell-sat-11th-mar-2023/, https://www.wmrt.org.uk/incidents/brown-tongue-scafell-pike-thu-1st-jan-1970/
    
    data.loc[data['Incident_Cause']=='','Incident_Cause']='Other' 
    # based on the mean number of staff of the full callout and limited callout - 15 vs 7, current data only 6 count of callout which is quite seprate, 2, 4, then 11 , so use 10 as cut off
    data.loc[(data['Incident_Type']=='Callout') & (data['staff'] >=10),'Incident_Type']='Full Callout'
    data.loc[(data['Incident_Type']=='Callout') & (data['staff'] <10),'Incident_Type']='Limited Callout'
    # missing data on Incident_Type, I read through and assign based on my judgement
    data.loc[data["Incident"]=='106 in 2025', 'Incident_Type']='Alert'
    data.loc[data["Incident"]=='38 in 2025', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='87 in 2025', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='133 in 2023', 'Incident_Type']='Alert'
    data.loc[data["Incident"]=='95 in 2023', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='55 in 2023', 'Incident_Type']='Limited Callout'
    # odd number of staff for small alerts due to the big number of staff around for other incidents or training, change the number to reflect based on reading of incident reports
    # to avoid inflation of total_hrs 
    data.loc[data["Incident"]=='117 in 2025', 'staff'] = 1
    data.loc[data["Incident"]=='117 in 2025', 'total_hrs'] = 2.6
    data.loc[data["Incident"]=='2 in 2023', 'staff'] = 1
    data.loc[data["Incident"]=='2 in 2023', 'total_hrs'] = 0.6
    data.loc[data["Incident"]=='121 in 2021', 'staff'] = 1
    data.loc[data["Incident"]=='121 in 2021', 'total_hrs'] = 4.3
    # replace with mean number of staff as again training nearby with 22 members
    data.loc[data["Incident"]=='57 in 2017', 'staff'] = 7
    data.loc[data["Incident"]=='57 in 2017', 'total_hrs'] = 20.3
    # drop rows with hrs or staff as NaN, most are either short alert or flood responding rather than mountain rescue
    data = data.dropna(subset=['hrs','staff','date'])

    return data
    
def convert_to_numeric(data):
    # data['hrs'] = data['hrs'].astype(float)
    # data['total_hrs'] = data['total_hrs'].astype(float)
    # data['staff'] = data['staff'].astype(int)
    data['hrs'] = pd.to_numeric(data['hrs'], errors='coerce')
    data['total_hrs'] = pd.to_numeric(data['total_hrs'], errors='coerce')
    data['staff'] = pd.to_numeric(data['staff'], errors='coerce')    
    return data

def calculating_other_agencies(data):
    data['Agencies_count'] = data['Other Agencies'].apply(lambda x: len(x) if type(x) == list else 0)
    return data

def determine_next_day(data):
    data['start_time_obj'] = pd.to_datetime(data['start_time'], format = "%H:%M")
    data['end_time_obj'] = pd.to_datetime(data['end_time'], format = "%H:%M")

    # to add one day delta to the end time if it ends in the next day
    data['next_day'] = data['end_time_obj'] < data['start_time_obj']   

    return data

def preprocess_data():
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)
    data = data[(data['year']>2014) & (data['year']<2026)]
    return data