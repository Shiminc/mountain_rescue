import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

# faceted plot split by month

def trend_across_years(df,month_input):
    data = df[df['month']==month_input]
    chart = alt.Chart(data).mark_area().encode(
        alt.X('year:O'),
        alt.Y('Incident:Q'),
        # column='month:O'
    ).properties(
    width=80,
    height=100)

    rule = alt.Chart(data).mark_rule().encode(
        y='mean(Incident):Q'
    )

    return chart + rule

def trend_year(df):
    chart = alt.Chart(df).mark_line(point=True).encode(
        alt.X('month:O'),
        alt.Y('Incident:Q'),
        alt.Color('year:N')
    )

    month_ave = alt.Chart(df).mark_line(point=True,size=5).encode(
        alt.X('month:O'),
        alt.Y('mean(Incident):Q'), 
    )

    return (chart + month_ave).properties(
    width=800,
    height=1000)

def main():
    set_up_altair()
    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)

    chart = trend_across_years(incident_count, 1)
    for month in range(2,13):
        chart =(chart | trend_across_years(incident_count, month)).resolve_scale(y='shared')
        
 

    # chart = trend_year(incident_count)

    chart.show()
    print('finish')


main()