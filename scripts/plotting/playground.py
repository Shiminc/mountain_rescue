import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import numpy as np
import pandas as pd
import json
from datetime import timedelta, date, datetime 
import altair as alt
from altair import datum

def generate_calendar(start_date='2025-01-01', end_date='2025-12-31', freq='D'):
    index = pd.date_range(start_date, end_date, freq=freq)
    base = np.zeros((len(index),))

    base_frame = pd.DataFrame({'Date':index,'Count':base})
    return base_frame

def bubble(data):
    chart = alt.Chart(data).mark_circle(opacity = 0.4).encode(
        alt.X('day',scale = alt.Scale(domain = (0,31))),
        alt.Y('month(date):T'),
        alt.Size('total_hrs'),
        alt.Color('Incident_Cause'),
    )
    return chart

def heatmap(data):
    chart = alt.Chart(data).mark_rect().encode(
        alt.X('day'),
        alt.Y('month'),
        alt.Color('total_hrs'),
    )
    return chart

def main():
    set_up_altair()
    data = preprocess_data()
    data = data[data['year'] == 2025]

    trial = generate_calendar()

    bubble(data).show()
    print('finish')

main()