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
        alt.Color('Incident_Cause:N').title('Incident Cause').legend(),
        alt.Size('total_hrs').scale(bins=[0,50,100,200,400,800]).title('total hours').legend(orient='right'),
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

def cause_bar(data):
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('count()').title(None),
        alt.Y('Incident_Cause:N').sort('-x').title(None),
        alt.Color('Incident_Cause:N').legend(None),
    )

    return chart


def week_bar(data):
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('count()').title(None),
        alt.Y('dayofweek_n', sort=['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).title(None),
        alt.Color('Incident_Cause:N').legend(None),
        tooltip =[
            alt.Tooltip(field="Incident_Cause"),
            alt.Tooltip('count()', title='Count of Incidents')  
        ],
    )
    return chart

def stacked_horizon(data):

    stacked_bar = alt.Chart(data,
                            title = alt.Title('Total number of Incidents in each year',
                                              orient = 'bottom')
                            ).mark_bar().encode(
        alt.X('count()').sort('descending').title(None),
        # alt.X('count()').title(None),
        alt.Y('year(date):T').axis(None),
        # alt.Y('year(date):T').title(None),
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

def monthly_bar_caption():
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
    
def main():
    set_up_altair()
    data = preprocess_data()
    # bubble(data).save('../../charts/main_chart.json')
    # alt.concat(stacked_horizon(data),bubble(data),  spacing=5).show()
    # alt.concat((bubble(data) & monthly_bar(data)).resolve_scale(x='shared'), stacked_horizon(data) & stacked_horizon_caption(),spacing=-5).show()
    alt.concat(stacked_horizon(data) & stacked_horizon_caption(),
                 (bubble(data) & (monthly_bar(data))).resolve_scale(x='shared'),
                #  (monthly_bar_caption()),
                #  (cause_bar(data) & week_bar(data)),
                 spacing=-2).save('../../charts/main_chart.json')

    # ((bubble(data)|(stacked_horizon(data) & stacked_horizon_caption())) & monthly_bar(data)).resolve_scale(x='shared').show()
 
    
    print('finish')


main()