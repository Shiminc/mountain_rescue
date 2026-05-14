import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np
import pmdarima as pm
import statsmodels.tsa.stattools as ts
from sklearn.metrics import mean_absolute_error as MAE
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle

rule_data = pd.DataFrame(
    [
        {"date": '01-01-2015'},
        {"date": '01-01-2016'},
        {"date": '01-01-2017'},
        {"date": '01-01-2018'},
        {"date": '01-01-2019'},
        {"date": '01-01-2020'},
        {"date": '01-01-2021'},
        {"date": '01-01-2022'},
        {"date": '01-01-2023'},
        {"date": '01-01-2024'},
        {"date": '01-01-2025'},

    ]
    )

def draw_forecast(existing_series,  predicted_series, conf_int_series):
    conf_df = conf_int_series.reset_index()
    conf_df.columns=['dateTime','lower Incident','upper Incident']

    pred_df = predicted_series.reset_index()
    pred_df['category'] ='forecast'
    pred_df.columns=['dateTime','Incident','category']


    prediction = pd.merge(conf_df, pred_df, on = 'dateTime')

    existing_df = existing_series.reset_index()
    existing_df['category'] ='past'
    existing_df.columns=['dateTime','Incident','category']


    band = alt.Chart(prediction).mark_errorband().encode(
    # band = alt.Chart(conf_df).mark_area(opacity = 0.3, color = '#57A44C').encode(
        alt.X('yearmonth(dateTime)').title(None),
        alt.Y('upper Incident').title('Number of Incidents'),
        alt.Y2('lower Incident'),
        tooltip = [
            alt.Tooltip('yearmonth(dateTime)', title="Month"),
            alt.Tooltip(field = 'Incident', format = '.2', title="Predicted number of incident"),
              alt.Tooltip('upper Incident', title="upper bound of the predicted value", format = '.2'),
            alt.Tooltip('lower Incident', title="lower bound of the predicted value", format = '.2')

        ]

    )

    forecast_line = alt.Chart(pred_df).mark_line(strokeDash=[5,5], size = 2, color='purple').encode(
        alt.X('yearmonth(dateTime)').title(None),
        alt.Y('Incident').title('Number of Incidents'),
        
    )

    forecast_point = alt.Chart(pred_df).mark_point(color = 'purple', filled=True).encode(
        alt.X('yearmonth(dateTime)').title(None),
        alt.Y('Incident').title('Number of Incidents'),
        tooltip = [
            alt.Tooltip('yearmonth(dateTime)', title="Month"),
            alt.Tooltip(field = 'Incident', format = '.2', title="Predicted number of incident")

        ]
    )

    existing_line = alt.Chart(existing_df, title = 'Number of Incidents each month between 2015 and 2025 and predicted number in 2026').mark_line().encode(
        alt.X('yearmonth(dateTime)').title(None),
        alt.Y('Incident').title('Number of Incidents'),
                tooltip = [
            alt.Tooltip('yearmonth(dateTime)', title="Month"),
            alt.Tooltip(field = 'Incident')

        ]
    )

    year_rule = alt.Chart(rule_data).mark_rule(color='black',opacity=0.2).encode(
        alt.X('yearmonth(date):T').title(None))


    return (band + forecast_line + forecast_point + existing_line + year_rule).properties(
    width=1500,
    height=300)


def main():
    set_up_altair()
    data = preprocess_data()


    incident_count = aggregate_by_year_month(data)
    # incident_count.to_json('trend.json', orient='records')

    incident_count.set_index('dateTime', inplace=True)
    full_series = incident_count.Incident

    forecast_value = pd.read_pickle('forecast_value.pkl')
    forecast_conf_int = pd.read_pickle('forecast_conf_int.pkl')

    draw_forecast(full_series, forecast_value, forecast_conf_int).show()
    draw_forecast(full_series, forecast_value, forecast_conf_int).save('../../charts/prediction.json')


    print('finish')
main()