import pandas as pd
import json
from datetime import timedelta, date, datetime 
import altair as alt
from altair import datum


PATH = 'all_incidents.json'

def load_data():
    with open(PATH, 'r') as json_file:
        data = json.load(json_file)
    return pd.DataFrame(data)

def format_datetime(data):
    data['date'] = pd.to_datetime(data['date'], format = "%d %b %Y" )


    data['start_time_obj'] = pd.to_datetime(data['start_time'], format = "%H:%M")
    data['end_time_obj'] = pd.to_datetime(data['end_time'], format = "%H:%M")

    # to add one day delta to the end time if it ends in the next day
    data['next_day'] = data['end_time_obj'] < data['start_time_obj']   
    data.loc[data['next_day'] == True,'end_time_obj'] =  data['end_time_obj'] +  pd.Timedelta(days=1)


    # calculate time used
    data['time_used'] = data['end_time_obj'] - data['start_time_obj']
    # data['time_used'] = data['time_used'].total_seconds()
    data['time_used'] = data['time_used'].apply(pd.Timedelta.total_seconds)
    # turn seconds to hours
    data['time_used'] = data['time_used']/3600

    # convert start time and end time to float and based on from '1900-01-01T00:00:00'
    base_datetime = datetime.strptime('01 Jan 1900', "%d %b %Y")
    data['start'] = data['start_time_obj'] - base_datetime
    data['start'] = (data['start'].apply(pd.Timedelta.total_seconds))/3600
    data['end'] = data['end_time_obj'] - base_datetime
    data['end'] = (data['end'].apply(pd.Timedelta.total_seconds))/3600

    return data

def set_up_altair():
    alt.renderers.enable('browser')
    alt.data_transformers.disable_max_rows()

def time_spent_plot(data):
    #print(data)
    base = alt.Chart(data).encode(
        color = 'Incident_Cause'
    ).transform_filter((datum.Incident_Cause != 'Other') & (datum.Incident_Cause != ''))

    axis_labels = ("datum.label == 0 ? '0 AM' : datum.label == 6 ? '6 AM' : datum.label == 12 ? '12 Noon' : datum.label == 18 ? '6 PM' : datum.label == 24 ? 'Next day' : datum.label == 30 ? '6 AM' : datum.label == 36 ? '12 Noon' : datum.label == 42 ? '6 PM' : datum.label == 48 ? '0 AM' : 'Others'") 
    start_point = base.mark_point().encode(
        x = alt.X('start', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])),
        y = alt.Y('yearmonth(date):T'),
        )
    
    end_point = base.mark_point().encode(
        x = alt.X('end', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])),
        y = alt.Y('yearmonth(date):T'),
        )

    start_end_line = base.mark_rule(strokeWidth=5).encode(
        x = alt.X('start'),
        x2 = 'end',
        y = alt.Y('yearmonth(date):T'),
    )
    
    return (start_point + end_point + start_end_line)

    #return (start_point + end_point + start_end_line )

def dual_axis_plot(data):
    base = alt.Chart(data).encode(
        alt.X('yearmonth(date):T').title(None)
        )

    sum_hrs = base.mark_line(color = 'red').encode(
        y = alt.Y('sum(time_used):Q')
    ) 

    count_incident = base.mark_line().encode(
        y = alt.Y('count():Q')
    )

    #chart = alt.layer(count_incident, sum_hrs).resolve_scale(y='independent')
    chart = count_incident
    return chart.configure_view(
    continuousWidth=1200,
    )


def main():
    set_up_altair()
    data = load_data()
    data = format_datetime(data)

    # use small dataset n = 10
    #data = data.sort_values(by=['time_used'],ascending=False).head(20)

    # cut off from 2000
    data = data[data['date']>pd.Timestamp(2012, 1, 1, 0) ]

    #chart = time_spent_plot(data)
    chart = dual_axis_plot(data)
    chart.show()
    print('finish')


main()