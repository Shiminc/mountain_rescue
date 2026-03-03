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
        alt.Color('Incident_Cause:N'),
        alt.Tooltip(['Incident_Cause','count()']),
    )
    return chart

# TODO colourblind colour, legend to show bar chart about how many cases in each cause, and side bar to show each year total 

def bubble(df):
   
    chart = alt.Chart(df, title='Incidents happened across the years').mark_circle(opacity=0.5, filled=True).encode(
        alt.X('monthdate(date):T').axis(format='%b').title(None),
        alt.Y('year(date):T').title(None),
        alt.Color('Incident_Cause:N'),
        alt.Size('total_hrs').scale(bins=[0,50,100,200,400,800]),
        alt.Tooltip(['Location','Incident_Cause','date','start_time','hrs','staff','Weather', 'Other Agencies']),
        href ='url'
    ).properties(
        width = 1000
    )
    return chart

# def bubble_other(df):
#     chart = alt.Chart(df).mark_circle(opacity=0.5, filled=True).encode(
#         alt.X('hrs'),
#         alt.Y('year(date):T'),
#         alt.Color('Incident_Cause:N'),
#         # alt.Size('total_hrs').scale(bins=[0,50,100,200,400,800]),
#         alt.Size('staff'),
#         alt.Tooltip(['Location','date','start_time','hrs','staff','Weather', 'Other Agencies']),
#         href ='url'
#     ).transform_calculate(
#     # Generate Gaussian jitter with a Box-Muller transform
#     jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
#     ).properties(
#         width = 1000
#     )
#     return chart

def stacked_horizon(data):

    stacked_bar = alt.Chart(data, title='Total number of incidents in each year').mark_bar().encode(
        alt.X('count()').sort('descending').title('Count of Incidents'),
        alt.Y('year(date):T').axis(None),
        alt.Color('Incident_Cause:N'),
        tooltip =[
            alt.Tooltip(field="Incident_Cause"),
            alt.Tooltip('count()', title='Count of Incidents')  
        ],
    )
    return (stacked_bar)

def stacked_horizon_caption():
    caption = alt.Chart().mark_text(
        align =  "left",
        baseline = "bottom",
        fontStyle='italic'
    ).encode(

        text = alt.value(['The number of incidents jumped in 2021 and generally',
                          'attributed to revenge tourism after Covid lockdown.',
                            'However it never regressed to pre-Covid times.']) 
    )
    return caption

def monthly_bar(data):
    bar = alt.Chart(data,
                    title = alt.Title(
                        'Total numbers of incident in months',
                        subtitle = 'Summing across 2015-2025',
                        orient = 'bottom'
                    )
                    ).mark_bar().encode(
        alt.Y('count()').sort('descending').title('Count of Incidents'),
        alt.X('month(date):T').axis(None),
        alt.Color('Incident_Cause:N'),
        tooltip =[
            alt.Tooltip(field="Incident_Cause"),
            alt.Tooltip('count()', title='Count of Incidents')  
        ],
    ).properties(
        height=100
    )
    return bar

def main():
    set_up_altair()
    data = preprocess_data()
    # bubble(data).save('main_chart.json')
    # alt.concat(stacked_horizon(data),bubble(data),  spacing=5).show()
    alt.concat(stacked_horizon(data) & stacked_horizon_caption(),(bubble(data) & monthly_bar(data)).resolve_scale(x='shared'),spacing=-5).show()
    # (monthly_bar(data) & (bubble(data)|stacked_horizon(data))).show()
    print('finish')


main()