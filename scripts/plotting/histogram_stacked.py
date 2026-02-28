import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt

# histogram of each variables

def create_stacked_bar(df, var_x, stacked_var):
    string_y = 'count(' + stacked_var + ')'
    bar_chart = alt.Chart(df).mark_bar().encode(
        alt.X(var_x),
        alt.Y(string_y),
        color = stacked_var,
        tooltip=([var_x, string_y])

    )

    return bar_chart


def histogram(df,var_x:str):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(var_x),
        alt.Y('count():Q'),
        tooltip=([var_x,'count()'])
    )
    return chart

def histogram_time(df,var_x:str):
    string_x = var_x + ':T'
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(string_x),
        alt.Y('count():Q'),
        alt.Color('Incident_Cause'),
        tooltip=([var_x,'count()'])
    )
    return chart

def sorted_bar(df,var_x:str):
    df = df.explode([var_x])
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(var_x).sort('-y'),
        alt.Y('count(Incident_Cause):Q'),
        alt.Color('Incident_Cause'),
        tooltip=([var_x,'count(Incident_Cause)'])
    )
    return chart

def main():
    set_up_altair()
    data = preprocess_data()

    ((create_stacked_bar(data,'hrs','Incident_Cause') |  histogram(data,'total_hrs'))
      & (histogram(data,'staff') | histogram(data,'Agencies_count'))
      & (histogram(data,'next_day') | histogram(data,'Incident_Type') | histogram(data,'Incident_Cause')) 
      & (sorted_bar(data,'year') | sorted_bar(data,'month'))
      & (histogram_time(data,'end_time_obj')|histogram_time(data,'start_time_obj'))
      & (sorted_bar(data,'Weather'))
      & (sorted_bar(data,'Other Agencies'))
      & (sorted_bar(data,'Diagnosis'))
      ).show()


    print('finish')


main()