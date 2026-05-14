import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
# from utils.utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd
import altair as alt
from datetime import datetime

axis_labels = "datum.label == 0 ? '0 AM' : datum.label == 6 ? '6 AM' : datum.label == 12 ? '12 Noon' : datum.label == 18 ? '6 PM' : datum.label == 24 ? 'Next day' : datum.label == 30 ? '6 AM' : datum.label == 36 ? '12 Noon' : datum.label == 42 ? '6 PM' : datum.label == 48 ? '0 AM' : 'Others'" 

def weather_time_chart(df):

    chart = alt.Chart(df).mark_circle(opacity=0.5, filled=True).encode(
        alt.Y('start_hour', axis=alt.Axis(values=[0,6,12,18,24])).sort('ascending').title('Start Time'),
        alt.X('monthdate(date):T'),
        alt.Color('Weather',scale=alt.Scale(scheme="tableau20"))
    )

    return chart

def weather_gantt(df):
    selection_weather = alt.selection_point(fields=['Weather'], value=[{'Weather': 'Rain'}])
    selection_year = alt.selection_point(fields=['year'], value=[{'year': 2025}])

    color_year = (
        alt.when(selection_year)
        # .then(alt.Color('year:N').legend(None))
        .then(alt.value("darkgrey"))
        .otherwise(alt.value("lightgray"))
        )
    
    color_weather = (
        alt.when(selection_weather)
        .then(alt.Color('Weather:N').legend(None))
        .otherwise(alt.value("lightgray"))
        )
    
    legend_year = alt.Chart(df).mark_rect().encode(
        alt.Y('year:N').axis(title = 'Year', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        # color = alt.Color('year').legend(None)
        color=color_year
    ).add_params(
        selection_year,
    ).resolve_legend(color = 'independent')
    
    legend_weather = alt.Chart(df).mark_rect().encode(
        alt.Y('Weather:N').axis(title = 'Weather', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        # color = alt.Color('year').legend(None)
        color=color_weather
    ).add_params(
        selection_weather,
    ).resolve_legend(color = 'independent')

    base = alt.Chart(df).mark_line(size=3,opacity=0.5).encode(
        alt.X('start_hour', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])).title(None),
        alt.X2('end_hour').title(None),
        # alt.Y('monthdate(date):T').axis(format='%b').title(None),
        alt.Y('start_hour', axis=alt.Axis(values=[0,6,12,18,24])).sort('ascending').title('Start Time'),
        alt.Tooltip(['Location','Incident_Cause','date','start_time','end_time','hrs','staff']),
        href ='url',
        color = alt.Color('Weather',scale=alt.Scale(scheme="tableau20"))

    ).transform_filter(
    selection_weather & selection_year
    )
    return base | legend_weather | legend_year

def main():
    set_up_altair()
    data = preprocess_data()
    df = data.explode(['Weather'])
    # before 2018 weather is null
    df = df[df['year']>2018]
    weather_time_chart(df).show()
    weather_gantt(df).show()
    print('finish')


main()