from scripts.utils.utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd
import altair as alt

PATH = "../../data/all_incidents.json"

def tick_dash(df):
    chart = alt.Chart(df).mark_tick().encode(
        alt.X('dayofyear(date):T'),
        alt.Y('year(date):T'),
        color = alt.Color('Incident_Cause:N')
    )
    return chart

def bubble(df):
    chart = alt.Chart(df).mark_point(opacity=0.5, filled=True).encode(
        alt.X('monthdate(date):T'),
        alt.Y('year(date):T'),
        color = alt.Color('Incident_Cause:N'),
        size = alt.Size('hrs')
    ).properties(
        width = 1000
    )
    return chart

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
 
    chart = alt.Chart(df).mark_bar().encode(
        alt.X('start_time:T'),
        alt.X2('end_time:T'),
        alt.Y('year:O'),
        alt.Color('Incident_Cause:N')
    ).properties(
        width = 1000,
        height = 500
    )

    return chart




def main():
    set_up_altair()

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data.loc[data['Incident_Cause'] == '','Incident_Cause'] = 'Other'
    data = data[data['date']>pd.Timestamp(2015, 1, 1, 0) ]

    data['hrs'] = data['hrs'].astype(float)
    data['total_hrs'] = data['total_hrs'].astype(float)
    # tick_dash(data).show()
    # bubble(data).show()
    data = format_end_time(data)
    gantt_chart(data).show()
    print('finish')


main()