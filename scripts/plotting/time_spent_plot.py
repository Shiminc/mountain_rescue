import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month

import pandas as pd
import json
from datetime import timedelta, date, datetime 
import altair as alt
from altair import datum


def set_up_altair():
    alt.renderers.enable('browser')
    alt.data_transformers.disable_max_rows()

def time_spent_plot(data):
   
    base = alt.Chart(data).encode(
        color = 'Incident_Cause'
    )
    # ).transform_filter((datum.Incident_Cause != 'Other') & (datum.Incident_Cause != ''))

    
    axis_labels = ("datum.label == 0 ? '0 AM' : datum.label == 6 ? '6 AM' : datum.label == 12 ? '12 Noon' : datum.label == 18 ? '6 PM' : datum.label == 24 ? 'Next day' : datum.label == 30 ? '6 AM' : datum.label == 36 ? '12 Noon' : datum.label == 42 ? '6 PM' : datum.label == 48 ? '0 AM' : 'Others'") 
    start_point = base.mark_point().encode(
        x = alt.X('start_hour', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])),
        y = alt.Y('yearmonthdate(date):T').axis(format='%b').title(None),
        )
    
    end_point = base.mark_point().encode(
        x = alt.X('end_hour', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])),
        y = alt.Y('yearmonthdate(date):T').axis(format='%b').title(None),
        )

    start_end_line = base.mark_rule(strokeWidth=2).encode(
        x = alt.X('start_hour'),
        x2 = 'end_hour',
        y = alt.Y('yearmonthdate(date):T'),
    )

    next_day_rule = alt.Chart().mark_rule(color='grey',opacity=0.5).encode(
       x=alt.datum(24)
    )
    return (start_point + end_point + start_end_line + next_day_rule).properties(height=500)
    # return start_end_line

# def dual_axis_plot(data):
#     base = alt.Chart(data).encode(
#         alt.X('yearmonth(date):T').title(None)
#         )

#     sum_hrs = base.mark_line(color = 'red').encode(
#         y = alt.Y('sum(time_used):Q')
#     ) 

#     count_incident = base.mark_line().encode(
#         y = alt.Y('count():Q')
#     )

#     #chart = alt.layer(count_incident, sum_hrs).resolve_scale(y='independent')
#     chart = count_incident
#     return chart.configure_view(
#     continuousWidth=1200,
#     )


def main():
    set_up_altair()
    data = preprocess_data()
    # data = data[data['year']==2025]
    chart = time_spent_plot(data)
    # chart = dual_axis_plot(data)
    chart.show()
    print('finish')


main()