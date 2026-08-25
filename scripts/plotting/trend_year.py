"""
bar chart showing hrs, total_hrs, staff in each year
similar trend in grand scheme

"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data
import altair as alt

#x axis by year, count of incident then hrs/staff/total_hrs


def create_bar_line(df,time='year'):
    if time == 'year':
        x_var = 'year(date)'
    elif time == 'yearmonth':
        x_var = 'yearmonth(date)'

    bar_chart = alt.Chart(df).mark_bar().encode(
        x = x_var,
        y = 'count(Incident_Cause)',
        color = 'Incident_Cause:N'
    )
    line_chart = alt.Chart(df).mark_line(color='black').encode(
        x = x_var,
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

def main():
    set_up_altair_browser()
    data = preprocess_data()


    # create_bar_line(data, time='yearmonth').show()
    create_stacked_bar(data).show()

    print('finish')


main()
