from utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

PATH = "../../data/all_incidents.json"


def aggregate_by_year_month_hrs(df, start_date='2015-01-01', end_date='2025-11-01', freq='MS'):
    #create a dummy series that include all date so that when we merge with the data, any month without any incident will be able to filled with 0
    index = pd.date_range(start_date, end_date, freq=freq)
    dummy_series = pd.Series(index=index,name='dummy')

    df['total_hrs'] = df['total_hrs'].astype(float)
    df['total_hrs'] = df['total_hrs'].astype(float)


    total_hrs_average = df.pivot_table(index=['year_month'],
                              #columns='Incident_Type',
                              values='total_hrs',
                              aggfunc='sum', 
                              fill_value=0)
                              #margins=True
    merged_df = pd.merge(dummy_series, total_hrs_average, how = 'left', left_index=True, right_index=True)
    merged_df.drop(labels='dummy', axis='columns', inplace=True)
    merged_df.fillna(0,inplace=True)
    merged_df.reset_index(inplace=True)
    merged_df.columns=['dateTime','total_hrs_average']
    merged_df['year']=merged_df.dateTime.dt.year
    merged_df['month']=merged_df.dateTime.dt.month
    merged_df['year_month']= pd.to_datetime(merged_df['dateTime'], format = "%Y-%m-%d").astype(str)
    merged_df['moving_average']=moving_averages(merged_df.total_hrs_average,12)
    return merged_df


def create_year_month_line(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('year_month:T'),
        alt.Y('total_hrs_average:Q'),
    ).properties(
    width=1000,
    height=300)
    return line_overall



def main():
    set_up_altair()

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    total_hrs_average = aggregate_by_year_month_hrs(data)
    create_year_month_line(total_hrs_average).show()
    print('finish')


main()