# year_month trend line with moving average of past 12 months
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  aggregate_by_year_month

import pandas as pd
import altair as alt




def create_year_month_line(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('year_month:T'),
        alt.Y('Incident:Q'),
    ).properties(
    width=1000,
    height=300)
    return line_overall

def create_year_month_line_smooth(df):
    line_overall = alt.Chart(df).mark_line(point=False, color='red').encode(
        alt.X('year_month:T'),
        alt.Y('moving_average:Q'),
    ).properties(
    width=1000,
    height=300)

    return line_overall

def create_year_line_chart(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('year:O'),
        alt.Y('sum(Incident):Q')
    )
    return line_overall

# like spaghetti cos 10 categories
def create_month_year_cat_line(df):
    line_overall = alt.Chart(df).mark_line(point=True).encode(
        alt.X('month:O'),
        alt.Y('Incident:Q'),
        alt.Color('year:O')
    )
    return line_overall


def main():
    set_up_altair_browser()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    

    # create_year_line_chart(incident_count).show()
    (create_year_month_line(incident_count) + create_year_month_line_smooth(incident_count)).show()
    print('finish')


main()
