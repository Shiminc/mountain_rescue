import pandas as pd
import json
import time
from datetime import timedelta, date, datetime 
import numpy as np
import altair as alt

def set_up_altair():
    alt.renderers.enable('browser')
    #alt.renderers.enable('mimetype') # offline renderer
    alt.data_transformers.disable_max_rows()


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

    # initial cleaning
    data_pd.dropna(subset=['date'],inplace=True)
    data_pd.reset_index(inplace=True)
    data_pd.drop(labels=['index'], axis='columns',inplace=True)
    # data_pd.drop_duplicates() methods not working
    return data_pd

def format_time_columns(df):
    df['date'] = pd.to_datetime(df['date'], format='%d %b %Y')
    df.sort_values(by=['date'])
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



def main():
    trial_series = np.random.rand(10)
    window = 3
    new_series = (moving_averages(trial_series, window))
    print(len(new_series))
main()