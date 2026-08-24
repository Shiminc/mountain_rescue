# histogram of hrs, total_hrs, staff for each cause

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data
import altair as alt


def faceted_histogram(df, variable):
    chart = alt.Chart(df).mark_bar().encode(
        
        x = variable,
        y = 'count()',
    ).facet(
        row = alt.Row('Incident_Cause')
    )
    return chart
    

def main():
    set_up_altair_browser()
    data = preprocess_data()
    (faceted_histogram(data, variable ='total_hrs')|faceted_histogram(data, variable ='hrs')|faceted_histogram(data, variable ='staff')).show()

    print('finish')

main()