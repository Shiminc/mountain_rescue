import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser, create_year_month_line_chart
from utils.utils import preprocess_data,  convert_day_to_word
import numpy as np
import pandas as pd
import json
from datetime import timedelta, date, datetime 
import altair as alt
from altair import datum

def aggregate_by_week_dayofweek(data):
    data = convert_day_to_word(data)

    week_day_df = data.groupby(['week_number','year','dayofweek','dayofweek_n'])['Incident_Cause'].count()
    week_day_df = week_day_df.reset_index()
    return week_day_df.groupby(by=['dayofweek','dayofweek_n'])['Incident_Cause'].agg(['sum','mean','median','min','max','std'])

def main():
    set_up_altair_browser()
    data = preprocess_data()
    dayofweek = aggregate_by_week_dayofweek(data)
    print('finish')
main()