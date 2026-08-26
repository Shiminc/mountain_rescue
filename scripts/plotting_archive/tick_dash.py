import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data

import altair as alt
# zoom in zoom out
# various plot to show trends with month and year as x, y axis, heatmap, bubble, tick-dash

def tick_dash(df):
    chart = alt.Chart(df).mark_tick().encode(
        alt.X('dayofyear(date):T'),
        alt.Y('year(date):T'),
        alt.Color('Incident_Cause:N'),
        alt.Tooltip(['Incident_Cause','count()']),
    )
    return chart


def cause_bar(data):
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('count()').title(None),
        alt.Y('Incident_Cause:N').sort('-x').title(None),
        alt.Color('Incident_Cause:N').legend(None),
    )

    return chart


def main():
    set_up_altair_browser()
    data = preprocess_data()
    tick_dash(data).show()
    cause_bar(data).show()
    
main()