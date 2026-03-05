import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month

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

    heat_map = alt.Chart(data).mark_rect().encode(
        alt.X('month:O'),
        alt.Y('year:O',sort='descending'),
        alt.Color('Incident:Q')
)
    return heat_map

def main():
    set_up_altair()
    data = preprocess_data()

    tick_dash(data).show() 

    print('finish')


main()