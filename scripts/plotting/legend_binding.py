import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

# same as the interactive_line


def trend_year(df):
    selection = alt.selection_point(fields=['year'], value=[{'year': 2025}], bind= 'legend',nearest=True)
    # selection = alt.selection_point(encodings=['color'], value=[{'year': 2025}], nearest=True, empty=False)
    color = (
        alt.when(selection)
        .then(alt.Color("year:N").scale(scheme="tableau10"))
        .otherwise(alt.value("lightgray"))
        )

    chart = alt.Chart(df).mark_line(point=True, size = 5).encode(
        alt.X('month:O'),
        alt.Y('Incident:Q'),
        color = color,
        tooltip=alt.Tooltip(field='year', title=None),

    ).add_params(
        selection
    )

    month_ave = alt.Chart(df).mark_line(point=True,size=2, color = 'black', strokeDash=[4,2]).encode(
        alt.X('month:O'),
        alt.Y('mean(Incident):Q'),
    )

    return (chart + month_ave).properties(
    width=800,
    height=1000) 


def main():
    set_up_altair()
    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)

    chart = trend_year(incident_count)

    chart.show()
    print('finish')


main()