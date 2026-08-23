import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser, create_year_month_line_chart
from utils.utils import preprocess_data,  aggregate_by_year_month
import numpy as np
import pandas as pd
import json
from datetime import timedelta, date, datetime 
import altair as alt
from altair import datum

def boxplot_with_mean(data):
    # Note that the default value of the extent property is 1.5, which represents the convention of extending the whiskers to the furthest points within 1.5 * IQR from the first and third quartile.
    base = alt.Chart(data).encode(
        alt.X('month(dateTime):T')
    )
    boxplot = base.mark_boxplot().encode(
        alt.Y('Incident:Q')
    )

    mean_tick = base.mark_tick(color = 'black').encode(
    alt.Y('mean(Incident)')    )

    return boxplot + mean_tick

def monthly_bar(data):
    bar = alt.Chart(data).mark_bar().encode(
        alt.Y('mean(Incident)').title('Count of Incidents'),
        alt.X('month(dateTime):T').axis(None),
        # tooltip =[
        #     alt.Tooltip(field="Incident_Cause"),
        #     alt.Tooltip('count()', title='Count of Incidents')  
        # ],
    ).properties(
        height=100
    )


    return bar


def main():
    set_up_altair_browser()
    data = preprocess_data()
    data_year_month = aggregate_by_year_month(data)
    # descriptive stats
    data_year_month.groupby(by='month')['Incident'].agg(['sum','mean','median','min','max','std'])
    # boxplot
    boxplot_with_mean(data_year_month).show()
    # monthly_bar(data_year_month).show()
    # create_year_month_line_chart(data).show()
    print('finish')

main()