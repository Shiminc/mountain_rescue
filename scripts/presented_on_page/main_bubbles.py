"""
Create bubble chart and the marginal chart 
The bubble chart shows every single incident
The margin chart is align to show sum across the years and month
the chart saved to `charts` to be published on the webpage

"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data

import altair as alt
# zoom in zoom out
# various plot to show trends with month and year as x, y axis, heatmap, bubble, tick-dash


# TODO colourblind colour, legend to show bar chart about how many cases in each cause, and side bar to show each year total 

def bubble(df):
    chart = alt.Chart(df, title='Incidents happened across the years',
                      ).mark_circle(opacity=0.5, filled=True).encode(
        alt.X('monthdate(date):T').axis(format='%b').title(None),
        alt.Y('year(date):T').title(None),
        alt.Color('Incident_Cause:N').title('Incident Cause').legend(None),
        alt.Size('total_hrs').scale(bins=[0,50,100,200,400,800]).title('total hours').legend(orient='right'),
        alt.Tooltip(['Location','Incident_Cause','date','start_time','hrs','staff','Weather', 'Other Agencies']),
        href ='url'
    ).properties(
        width = 1000
    )
    return chart


def stacked_horizon(data):

    stacked_bar = alt.Chart(data,
                            title = alt.Title('Number of Incidents in each year',
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
    ).properties(
        width = 300
    )
    return (stacked_bar)

def stacked_horizon_caption():
    caption = alt.Chart().mark_text(
        align =  "left",
        baseline = "bottom",
        fontStyle='italic'
    ).encode(

       text = alt.value(['The number of incidents jumped in',
                          '2021 and generally attributed to' ,
                          'revenge tourism after Covid lockdown.',
                          'However it never regressed to',
                          'pre-Covid times. Prior to that,',
                          'incidents peaked in 2017, driven',
                          'by unusually high number in Sep &',
                          'Oct (see heatmap below).'])
                          
    )
    return caption

def monthly_bar(data):
    bar = alt.Chart(data,
                    title = alt.Title(
                        'Total numbers of incident in each months',
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

        text = alt.value(['The number of incidents jumped in 2021',
                          'and generally attributed to revenge',
                          'tourism after Covid lockdown. However',
                          'it never regressed to pre-Covid times.'])
                          
    )
    return caption

def present_main_charts(data):
    chart = alt.concat(stacked_horizon(data) & stacked_horizon_caption(),
                  (bubble(data) & (monthly_bar(data))).resolve_scale(x='shared'),
                  spacing=-2)
    return chart

def main():
    set_up_altair_browser()
    data = preprocess_data()
    chart = present_main_charts(data)
    chart.show()
    chart.save('../../charts/main_chart.json')

 
    print('finish')


main()    