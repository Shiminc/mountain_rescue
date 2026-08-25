#plot to show the distribution of hours used in rescue (x), year in y-axis 
# each dot represents an incident

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data
from statsmodels.tsa.seasonal import STL as STL
import altair as alt
# TODO : choose with or without alert 

def beeswarm_plot(data, variable, title):
    beeswarm = alt.Chart(data, title = title).mark_point(filled=True, stroke='Black', strokeWidth=0.2).encode(
    # alt.Y('yearmonth(date):T'),
    alt.Y('year:O'),
    alt.X(variable),
    alt.Color('Incident_Cause:N'),
    yOffset="jitter:Q",

    ).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
    )

    mean_value = 'mean(' + variable +')'
    mean_line = alt.Chart(data).mark_tick(thickness=3,color='gray').encode(
    alt.Y('year:O'),
    alt.X(mean_value),
    )

    overall_mean = alt.Chart(data).mark_rule(thickness=1,color='gray').encode(
    x=alt.X(mean_value)
    )



    return beeswarm + mean_line + overall_mean

def main():
    set_up_altair_browser()
    data = preprocess_data()
        

    (beeswarm_plot(data,'hrs',title='Alert & Callout') &
     beeswarm_plot(data,'staff',title='Alert & Callout') &
     beeswarm_plot(data,'total_hrs',title='Alert & Callout')).show()
    print('finish')

main()