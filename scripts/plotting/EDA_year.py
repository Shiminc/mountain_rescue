import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

# double axis by year, count of incident then hrs/staff/total_hrs

def create_bar_line(df):
    bar_chart = alt.Chart(df).mark_bar().encode(
        x = 'year(date)',
        y = 'count(Incident_Cause)',
        color = 'Incident_Cause:N'
    )
    line_chart = alt.Chart(df).mark_line(color='black').encode(
        x = 'year(date)',
        y = 'sum(hrs)',
    )




    chart = (bar_chart + line_chart).resolve_scale(y='independent')

    return chart

def create_stacked_bar(df):
    bar_chart_cause = alt.Chart(df).mark_bar().encode(
        x = 'year(date)',
        y = 'count(Incident_Cause)',
        color = 'Incident_Cause:N'
    )

    bar_chart_hrs = alt.Chart(df).mark_bar().encode(
        x = 'year(date)',
        y = 'sum(hrs)',
        color = 'Incident_Cause:N'
    )

    bar_chart_total_hrs = alt.Chart(df).mark_bar().encode(
        x = 'year(date)',
        y = 'sum(total_hrs)',
        color = 'Incident_Cause:N'
    )

    return bar_chart_cause & bar_chart_hrs & bar_chart_total_hrs

def create_stacked_area(df):

    chart = alt.Chart(df).mark_area().encode(
       alt.X("yearmonth(date):T").axis(format="%Y", domain=False, tickSize=0),
       alt.Y('count(Incident_Cause)'),
        color = 'Incident_Cause:N' 
    )

    return chart.properties(width=1000)

def main():
    set_up_altair()
    data = preprocess_data()


    create_bar_line(data).show()
    create_stacked_bar(data).show()
    # create_stacked_area(data).show()

    print('finish')


main()
