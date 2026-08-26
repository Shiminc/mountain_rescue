"""
Look at incident numbers at the month level
Boxplot: showing the median and mean
bar chart: showing sum and the number of each incident cause
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt

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

    caption = alt.Chart().mark_text(
            align =  "left",
            baseline = "bottom",).encode(
            text = alt.value('White tick is median, black tick is mean')
            )

    return (boxplot + mean_tick) & caption

def monthly_bar(data):
    bar = alt.Chart(data,
                    title = alt.Title(
                        'Total numbers of incident in each months',
                        subtitle = 'Summing across 2015-2025',
                        orient = 'bottom'
                    )
                    ).mark_bar().encode(
        alt.Y('count()').title('Count of Incidents'),
        alt.X('month(date):T').axis(None),
        alt.Color('Incident_Cause:N'),
        tooltip =[
            alt.Tooltip(field="Incident_Cause"),
            alt.Tooltip('count()', title='Count of Incidents')  
        ],
    ).properties(
        height=100
    )
    return bar


def main():
    set_up_altair_browser()
    data = preprocess_data()
    data_year_month = aggregate_by_year_month(data)
    # descriptive stats
    print(data_year_month.groupby(by='month')['Incident'].agg(['sum','mean','median','min','max','std']))
    # each month numbers
    print(pd.crosstab(data['year'],data['month']))
    # boxplot and monthly_bar to show sum
    (boxplot_with_mean(data_year_month)& monthly_bar(data)).show()
    print('finish')

main()