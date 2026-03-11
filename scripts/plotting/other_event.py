import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month, convert_month_to_word,convert_day_to_word

import pandas as pd
import altair as alt


def tick_dash(df):
    chart = alt.Chart(df).mark_tick().encode(
        alt.X('dayofyear(date):T'),
        alt.Y('year(date):T'),
        color = alt.Color('Incident_Cause:N'),
    )
    return chart

def heat_map(df):
    data = aggregate_by_year_month(df)
    data = convert_month_to_word(data)
    heat_map = alt.Chart(data,
                      title = alt.Title(
                        'Total numbers of incident',
                        subtitle = 'in each month between 2015 - 2025',
                        orient = 'bottom'
                    )
                         ).mark_rect().encode(
        alt.X('month_n:N', sort=['Jan', 'Feb','Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep','Oct','Nov','Dec']).axis(labelAngle=0,labelFontSize=7).title(None),
        alt.Y('year:O',sort='descending').axis(labelFontSize=7).title(None),
        alt.Color('Incident:Q').scale(domain=[0,27]).legend().title(None),
        alt.Tooltip('Incident',title='Count of Incidents')
).properties(
    height = 140,
    width = 168
)
    return heat_map
def week_bar(data):
    data = convert_day_to_word(data)
    chart = alt.Chart(data,
                      title = alt.Title(
                        'Total numbers of incident',
                        subtitle = 'Summing across 2015 - 2025',
                        orient = 'bottom'
                    )
                      ).mark_bar().encode(
        alt.X('count()').title(None),
        alt.Y('dayofweek_n', sort=['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).title(None),
        alt.Color('Incident_Cause:N').legend(),
        tooltip =[
            alt.Tooltip(field="Incident_Cause"),
            alt.Tooltip('count()', title='Count of Incidents')  
        ],
    )
    return chart

def main():
    set_up_altair()
    data = preprocess_data()

    (week_bar(data)|heat_map(data)).save('../../charts/week.json')

    print('finish')


main()