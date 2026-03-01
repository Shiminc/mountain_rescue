import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month

import pandas as pd
import altair as alt

# various plot to show trends with month and year as x, y axis, heatmap, bubble, tick-dash

def tick_dash(df):
    chart = alt.Chart(df).mark_tick().encode(
        alt.X('dayofyear(date):T'),
        alt.Y('year(date):T'),
        color = alt.Color('Incident_Cause:N'),
    )
    return chart

# TODO colourblind colour, legend to show bar chart about how many cases in each cause, and side bar to show each year total 

def bubble(df):
    chart = alt.Chart(df).mark_circle(opacity=0.5, filled=True).encode(
        alt.X('monthdate(date):T'),
        # alt.X('dayofyear(date):T'),
        alt.Y('year(date):T'),
        color = alt.Color('Incident_Cause:N'),
        size = alt.Size('total_hrs').scale(bins=[0,50,100,200,400,800]),
        tooltip = alt.Tooltip(['Location','date','total_hrs']),
        href ='url'
    ).properties(
        width = 1000
    )
    return chart



def heat_map(df):
    data = aggregate_by_year_month(df)

    heat_map = alt.Chart(data).mark_rect().encode(
        alt.X('month:O'),
        alt.Y('year:O',sort='descending'),
        alt.Color('Incident:Q')
)
    return heat_map


def main():
    set_up_altair()
    data = preprocess_data()

    tick_dash(data).show() 
    # bubble(data).save('main_chart.json')
    bubble(data).show()
    # data = format_end_time(data)
    # gantt_chart(data).show()
    print('finish')


main()