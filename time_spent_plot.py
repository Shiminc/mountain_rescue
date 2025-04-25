import pandas as pd
import json
import time
from datetime import timedelta 
from datetime import date 
import altair as alt


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
    return data

def set_up_altair():
    alt.renderers.enable('browser')
    alt.data_transformers.disable_max_rows()

def time_spent_plot(data):
    base = alt.Chart(data).mark_point().encode(
    color = alt.Color('Incident_Cause')
    )

    start_point = base.mark_point().encode(
    x = alt.X('yearmonthdatehoursminutes(start_time_obj):T', axis = alt.Axis(labels=False), scale=alt.Scale(domain=['1900-01-01T00:00:00', '1900-01-03T00:00:00'])).title(None),
    #x = alt.X('yearmonthdatehoursminutes(start_time_obj):T', axis = alt.Axis(labels=False), timeUnit='yearmonthdatehours').title(None),

    y = alt.Y('date'),
    )

    end_point = base.mark_point().encode(
    x = alt.X('yearmonthdatehoursminutes(end_time_obj):T', axis = alt.Axis(labels=False), scale=alt.Scale(domain=['1900-01-01T00:00:00', '1900-01-03T00:00:00'])).title(None),
    y = alt.Y('date'),
    )

    start_end_line = base.mark_rule().encode(
    x = alt.X('start_time_obj', axis = alt.Axis(labels=False)).title(None),
    x2 = 'end_time_obj',
    y = alt.Y('date'),
    strokeWidth='staff:Q'
    )

    # mark the next day
    rule = base.mark_rule(strokeDash=[2, 2]).encode(
    x = alt.datum(alt.DateTime(year=1900, month = 1, date = 2, hours = 0)),
    color=alt.value("red")
    )

    # label for the next day
    label = rule.mark_text(
        text = 'Next day',
        dx = 35,
        baseline = 'bottom'
    )

    xaxis_label =  pd.DataFrame.from_dict({
        'timestamp' : ['1900-01-01T00:00:00', '1900-01-01T00:06:00', '1900-01-01T00:12:00', '1900-01-01T00:18:00', '1900-01-02T00:00:00','1900-01-02T00:06:00','1900-01-02T00:12:00','1900-01-02T00:18:00', '1900-01-03T00:00:00'],'label' : ['0 AM', '6 AM', '12 Noon', '6 PM', 'Next day', '6 AM', '12 Noon', '6 PM', '0 AM']})
    xaxis_label_chart = alt.Chart(xaxis_label).mark_text().encode(
        x = alt.X('timestamp:T', axis = alt.Axis(labels=False)).title(None),
        dx = 35,
        text = 'label'
    )
    xaxis_label_chart.show()

    return (start_point + end_point + start_end_line + rule + label)




def main():
    set_up_altair()
    data = load_data()
    data = format_datetime(data)

    # use small dataset
    data = data.sort_values(by=['time_used'],ascending=False).head(20)

    chart = time_spent_plot(data)
    chart.show()
    print('finish')


main()