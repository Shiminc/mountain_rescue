import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt


def faceted_histogram(df):
    chart = alt.Chart(df).mark_bar().encode(
        
        x = 'total_hrs',
        y = 'count()',
    ).facet(
        row = alt.Row('Incident_Cause')
    )
    return chart
    

def main():
    set_up_altair()
    data = preprocess_data()
    faceted_histogram(data).show()

    print('finish')

main()