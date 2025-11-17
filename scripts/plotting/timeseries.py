import pandas as pd
import json
import time
import altair as alt

PATH = 'all_incidents.json'

def set_up_altair():
    alt.renderers.enable('browser')
    #alt.renderers.enable('mimetype') # offline renderer
    alt.data_transformers.disable_max_rows()

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

def aggregate_by_year_month(df, start_date='2012-01-01', end_date='2025-06-01', freq='MS'):
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
    merged_df
    return merged_df

def create_year_month_line_chart(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('year_month:T'),
        alt.Y('Incident:Q')
    ).configure_axisTemporal


    return line_overall

def create_year_line_chart(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('year:O'),
        alt.Y('sum(Incident):Q')
    )
    return line_overall

def create_month_year_line(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('month:O'),
        alt.Y('Incident:Q'),
        alt.Color('year:O')
    )
    return line_overall

def main():
    set_up_altair()

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = filter_by_year(data, 2011)
    incident_count = aggregate_by_year_month(data)
    #chart_1 = create_year_month_line_chart(incident_count)
    #chart_2 = create_year_line_chart(incident_count)
    #chart_3 = create_month_year_line(incident_count)
    #alt.vconcat(chart_1, chart_2, chart_3).resolve_scale(color='independent', x='independent', y= 'independent').show()
    create_year_month_line_chart(incident_count).show()

    print('finish')


main()
