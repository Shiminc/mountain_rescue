import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  aggregate_by_year_month, convert_month_to_word,convert_day_to_word
from utils.variables import CAUSE_ORDER 
import pandas as pd
import altair as alt


def heat_map(df,title):
    data = aggregate_by_year_month(df)
    data = convert_month_to_word(data)
    heat_map = alt.Chart(data,
                      title = alt.Title(
                        title,
                        subtitle = 'in each month between 2015 - 2025',
                        orient = 'bottom'
                    )
                         ).mark_rect().encode(
        alt.X('month_n:N', sort=['Jan', 'Feb','Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep','Oct','Nov','Dec']).axis(labelAngle=0,labelFontSize=7).title(None),
        alt.Y('year:O',sort='descending').axis(labelFontSize=7).title(None),
        alt.Color('Incident:Q').scale(domain=[20,0],scheme='darkblue').legend().title(None),
        alt.Tooltip('Incident',title='Count of Incidents')
).properties(
    height = 140,
    width = 168
)
    return heat_map

def combine_chart(data):
    chart_list = []
    
    for cause in CAUSE_ORDER:
        data_cause = data.loc[(data['Incident_Cause']==cause)]
        chart_list.append(heat_map(data_cause,title=cause))

    
    return alt.vconcat(chart_list[0],chart_list[1],chart_list[2],chart_list[3],chart_list[4] )
def main():
    set_up_altair_browser()
    data = preprocess_data()

    chart = combine_chart(data)
    chart.show()

    print('finish')


main()