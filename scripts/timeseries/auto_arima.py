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


def auto_arima(timeseries):
    # the function return the best model so you don't need to create a new model with sarima with the params found. BUT realised the pdarima does not provide confidence level, so still better fit again with SARIMA
    # the model selected fulfil observation from acf, pacf
    stepwise_model = pm.auto_arima(timeseries, start_p=1, start_q=1,
                            max_p=3, max_q=3, m=12,
                            start_P=0, seasonal=True,
                            d=0, D=1, trace=True,
                            error_action='ignore',  
                            suppress_warnings=True, 
                            stepwise=True)
    print(stepwise_model.aic())
    stepwise_model.plot_diagnostics().show()
    print(stepwise_model.summary())
    # Ljung-box, Heteroskedasticity null hypo is normal dist
    # JB, skew, kurtosis further away from 0, more non-normal 
    #  you could just return the model, which will be the best model. BUT the pdarima.output does not provide confidence level, so still better fit again with SARIMA
    # return stepwise_model
    return (stepwise_model, stepwise_model.order, stepwise_model.seasonal_order)

def fit_final_model(order,seasonal_order, full_series):
    # https://www.statsmodels.org/dev/statespace.html#output-and-postestimation-methods-and-attributes
    final_model = SARIMAX(full_series,
                        order = order, 
                        seasonal_order = seasonal_order, 
                        ).fit()
    print('')
    print('final model fitted with full series')
    print(final_model.summary())

    return final_model

def forecast_future(model, timepoints):
    forecast_obj = model.get_forecast(steps=timepoints)
    forecast_conf_int = forecast_obj.conf_int(alpha = 0.05)
    forecast_value = forecast_obj.predicted_mean

    return forecast_value, forecast_conf_int

def draw_forecast(existing_series, fitted_series, predicted_series, conf_int_series):
    fitted_df = fitted_series.reset_index()
    fitted_df['category'] = 'fitted'
    fitted_df.columns=['dateTime','Incident','category']

    conf_df = conf_int_series.reset_index()
    conf_df.columns=['dateTime','lower Incident','upper Incident']

    pred_df = predicted_series.reset_index()
    pred_df['category'] ='forecast'
    pred_df.columns=['dateTime','Incident','category']

    existing_df = existing_series.reset_index()
    existing_df['category'] ='past'
    existing_df.columns=['dateTime','Incident','category']

    line_df = pd.concat([existing_df, pred_df])

    band = alt.Chart(conf_df).mark_errorband().encode(
    # band = alt.Chart(conf_df).mark_area(opacity = 0.3, color = '#57A44C').encode(
        alt.X('yearmonth(dateTime)'),
        alt.Y('upper Incident'),
        alt.Y2('lower Incident')
    )

    forecast_line = alt.Chart(pred_df).mark_line(strokeDash=[5,5], size = 2, color='purple').encode(
        alt.X('yearmonth(dateTime)'),
        alt.Y('Incident')
    )

    existing_line = alt.Chart(existing_df).mark_line().encode(
        alt.X('yearmonth(dateTime)'),
        alt.Y('Incident'),
        alt.Tooltip(['yearmonth(dateTime)','Incident'])
    )

    fitted_line = alt.Chart(fitted_df).mark_line(color = 'purple').encode(
        alt.X('yearmonth(dateTime)'),
        alt.Y('Incident'),
        alt.Tooltip(['yearmonth(dateTime)','Incident'])
    )

    return (band + forecast_line + existing_line + fitted_line).properties(
    width=1000,
    height=100)




def main():
    set_up_altair()
    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)

    # use 2025 as test data, 2015-2024 as train data
    train_data = incident_count[incident_count['year']<2025]
    test_data = incident_count[incident_count['year'] == 2025]
    
    full_series = incident_count.Incident
    train_series = train_data.Incident
    test_series = test_data.Incident

    # run auto_arima to know which model to use (after investigating the series with acf, pacf, stl decompose, and stationary)
    model, order, seasonal_order = auto_arima(train_series)

    # predict based on the length of the test data and evaluate the model, mainly used to compare to other models, like prophet, ML. 
    test_predicted = model.predict(len(test_series))
    print('')
    print('MAE of predicting 2025')
    print(MAE(test_series, test_predicted))

    # if this model is choosen, refit the model with the whole series, 2015-2025, then forecast 2026
    final_model = fit_final_model(order,seasonal_order, full_series)
    forecast_value, forecast_conf_int = forecast_future(final_model, 12)
    fitted_value = final_model.fittedvalues
    draw_forecast(full_series, fitted_value, forecast_value, forecast_conf_int).show()



    print('finish')

main()