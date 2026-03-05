import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

def format_end_time(df):
    df['end_time'] = pd.to_datetime(df['end_time'],format="%H:%M")
    df['start_time'] = pd.to_datetime(df['start_time'],format="%H:%M")

    # to add one day delta to the end time if it ends in the next day
    df['next_day'] = df['end_time'] < df['start_time']   
    # df.loc[df['next_day'] == True,'end_time'] =  df['end_time'] +  pd.Timedelta(days=1)

    for index, row in df.iterrows():
        if row['next_day']:
            # row['end_time'] = row['end_time'] + pd.Timedelta(days=1)
            df.loc[index, 'end_time'] = row['end_time'] + pd.Timedelta(days=1)
            
    # this_is_not_the_df = [row['end_time'] + pd.Timedelta(days=1) for row in df.iterrows() if row['next_day']]
    return df

def gantt_chart(df):
    data = df[df['year']==2025]
    chart = alt.Chart(data).mark_bar(opacity=0.5).encode(
        alt.X('start_time_obj:T'),
        alt.X2('end_time_obj:T'),
        alt.Y('monthdate(date):T'),
        alt.Color('Incident_Cause:N'),
        alt.Size('staff').legend(None)

    ).properties(
        width = 1000,
        height = 1000
    )

    return chart

def main():
    set_up_altair()
    data = preprocess_data()


    gantt_chart(data).show()
    print('finish')


main()