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
    # data = df[df['year']==2025]
    year_list = [2025,2024,2023,2022,2021, 2020,2019,2018,2017,2016,2015]
    # year_dropdown = alt.binding_select(options=year_list, name='Year')
    # year_select = alt.selection_point(fields=['year'],bind=year_dropdown)
    axis_labels = ("datum.label == 0 ? '0 AM' : datum.label == 6 ? '6 AM' : datum.label == 12 ? '12 Noon' : datum.label == 18 ? '6 PM' : datum.label == 24 ? 'Next day' : datum.label == 30 ? '6 AM' : datum.label == 36 ? '12 Noon' : datum.label == 42 ? '6 PM' : datum.label == 48 ? '0 AM' : 'Others'") 
    selection = alt.selection_point(fields=['year'], value=[{'year': 2025}])


    color = (
        alt.when(selection)
        .then(alt.Color('Incident_Cause:N').legend(None))
        .otherwise(alt.value("lightgray"))
        )
    
    legend = alt.Chart(df).mark_rect().encode(
        alt.Y('year:N').axis(title = 'Year', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        color = alt.Color('year').legend(None)     
    ).add_params(
        selection,
    ).resolve_legend(color = 'independent')


    base = alt.Chart(df).mark_line(size=2,opacity=0.5).encode(
        alt.X('start_hour', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])).title(None),
        alt.X2('end_hour').title(None),
        alt.Y('monthdate(date):T').axis(format='%b').title(None),
        color = color,
        # alt.Size('staff').legend(None)

    ).properties(
        height = 200,
        width = 200
    ).add_params(
        selection,
    )

    next_day_rule = alt.Chart().mark_rule(color='grey',opacity=0.5).encode(
       x=alt.datum(24)
    )


    return (base + next_day_rule)|legend

def top_20_hrs(data):
    year_list = list(data['year'].unique())
    for i, year in enumerate(year_list):
        temp_df = data[data['year'] == year]
        temp_df_top = temp_df.sort_values(by=['hrs'], ascending = False).head(20)
        if i == 0:
            df = temp_df_top
        else:
            df = pd.concat([df,temp_df_top])

    return df

def main():
    set_up_altair()
    data = preprocess_data()
        
    data=top_20_hrs(data)

    gantt_chart(data).show()

    print('finish')


main()