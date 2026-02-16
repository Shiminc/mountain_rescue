from scripts.utils.utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd
import altair as alt
from datetime import datetime
import json

PATH = "../../data/all_incidents.json"

def bar_chart(data):


    chart = alt.Chart(data).mark_bar().encode(
        alt.X('Incident_Cause:N'),
        alt.Y('count():Q')
    )


    return chart

def filter(path):

    with open(path) as f:
        data = json.load(f)

    filtered_data = [d for d in data if datetime.strptime(d['date'], "%d %b %Y") > datetime.strptime('31 Dec 2024', "%d %b %Y")]


    return filtered_data

def main():
    set_up_altair()


    filtered_data = filter(PATH)
    chart = bar_chart(filtered_data)
    
    chart.show() 
    

    print('finish')


main()