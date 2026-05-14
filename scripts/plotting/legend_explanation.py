import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month

import pandas as pd
import altair as alt

incident_cause = ['Cragfast','Injured & Medical','Lost','Other','Overdue']
pretend_x = [1,1,1,1,1]
incident_text = [
    'walkers being stuck at a spot and do not know how to move out of it, it could be on a steep slope or a craggy ravine or unstable screes',
    'walkers, their company, or passers-by calling for help when there is injury or medical conditions',
    'walkers calling for help when they could not find their way',
    'other events could include assisting local emergency, saving dog in distress on mountains, rescuing people from lakes, clearing road during winter, assisting flood rescues',
    'overdue is triggered when people reporting the walker(s) do not come back in time.'
]

legend_text = "datum.label == 'Cragfast' ? 'Cragfast - walkers being stuck at a spot and do not know how to move out of it, it could be on a steep slope or a craggy ravine or unstable screes': 'Other'"
def plot(data):
    chart = alt.Chart(data).mark_circle(opacity=0).encode(
        alt.Color('incident_cause:N').title('Incident Cause').legend(labelExpr = legend_text, labelFontSize=16, labelPadding=5),
    ).properties(view=alt.ViewConfig(stroke=None)).properties(
        width = 1000
    )
    return chart

def main():
    set_up_altair()
    data = pd.DataFrame({'incident_cause':incident_cause, 'pretend_x':pretend_x})
    plot(data).show()
    print('finish')


main()