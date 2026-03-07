import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np

PATH = "../../data/ukbankholidays-jul19.csv"

def create_season(df):
    df['season'] = 'season'
    df['season'][df['month'].isin([12,1,2])] ='winter'
    df['season'][df['month'].isin([3,4,5])] ='spring'
    df['season'][df['month'].isin([6,7,8])] ='summer'
    df['season'][df['month'].isin([9,10,11])] ='autumn'

    return df

# def create_temp(start_date='2015-01-01', end_date='2025-12-31', freq='MS'):
#     index = pd.date_range(start_date, end_date, freq=freq)

#     return ...

def count_bank_holidays():
    data = pd.read_csv(PATH)
    data = data[['UK BANK HOLIDAYS']].dropna()
    data.columns =['bankholidays']
    data['bankholidays'] = pd.to_datetime(data['bankholidays'], format='%d-%b-%Y')
    data['year'] = data['bankholidays'].dt.year
    data['month'] = data['bankholidays'].dt.month
    data = data[data['year']>=2015]
    data = data.groupby(['year', 'month'])['bankholidays'].count().to_frame().reset_index()
    data['year_month'] = data['year'].astype(str) + '-' + data['month'].astype(str)
    data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m')
    data = data[['year_month','bankholidays']]
    data.columns = ['dateTime','bankholidays']
    data = data.set_index('dateTime')
   
    return data

def count_weekenddays(start_date='2015-01-01', end_date='2025-12-31'):
    # The day of the week with Monday=0, Sunday=6.
    index = pd.date_range(start_date, end_date)
    days_of_week = pd.DataFrame({'Date':index, 'Year': index.year, 'Month':index.month,  'dayofweek': index.dayofweek})
    weekenddays = days_of_week[days_of_week['dayofweek']>=5]
    weekenddays_count = weekenddays.groupby(['Year', 'Month'])['Date'].count().to_frame().reset_index()
    weekenddays_count['year_month'] = weekenddays_count['Year'].astype(str) + '-' + weekenddays_count['Month'].astype(str)
    weekenddays_count['year_month'] = pd.to_datetime(weekenddays_count['year_month'], format='%Y-%m')
    data = weekenddays_count[['year_month', 'Date']]
    data.columns =['dateTime','count_of_weekend_days']
    data = data.set_index('dateTime')
    return data 

def create_features(incident_count):
    data = create_season(incident_count)

    weekenddays = count_weekenddays()
    bankholidays = count_bank_holidays()

    data = data.merge(weekenddays, how = 'left', on = 'dateTime').merge(bankholidays, how = 'left', on = 'dateTime').sort_index().fillna(0)
    return data 
# def main():
#     # set_up_altair()
#     data = preprocess_data()
#     incident_count = aggregate_by_year_month(data)
#     incident_count.set_index('dateTime', inplace=True)
    
#     data = create_season(incident_count)

#     weekenddays = count_weekenddays()
#     bankholidays = count_bank_holidays()

#     data = data.merge(weekenddays, how = 'left', on = 'dateTime').merge(bankholidays, how = 'left', on = 'dateTime').sort_index().fillna(0)
#     print('finish')

# main()