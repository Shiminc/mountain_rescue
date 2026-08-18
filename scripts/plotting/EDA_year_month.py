import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

# double y-axis by year_month to show count of incident and staff/hrs/total_hrs in the same chart to show trends

def create_stacked_bar(df):
    bar_chart = alt.Chart(df).mark_bar(width=5).encode(
        x = 'yearmonth(date)',
        y = 'count(Incident_Cause)',
        color = 'Incident_Cause:N'
    )
    
    line_chart = alt.Chart(df).mark_line(color='black').encode(
        x = 'yearmonth(date)',
        y = 'sum(hrs)',
    )

    year_list = []
    for year in range(2015, 2026):
        year_list.append({'year': pd.Timestamp(year, 1, 1, 0)})
    

    year_list = pd.DataFrame(year_list)
 
    year_line = alt.Chart(year_list).mark_rule(stroke="#000", strokeWidth=0.6, opacity=0.7).encode(
        alt.X("yearmonth(year)")
    )

    # chart = (bar_chart + line_chart).resolve_scale(y='independent')

    chart = (bar_chart + year_line + line_chart).properties(width = 1000).configure_axisX(title=None)
    return chart

def main():
    set_up_altair()
    data = preprocess_data()


    create_stacked_bar(data).show()
    print('finish')


main()
