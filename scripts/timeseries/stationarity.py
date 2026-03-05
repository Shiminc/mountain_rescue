import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss

# to test whether the series is stationary (i.e., equal means, variance). If non-stationary, SARIMA could be used by first differencing.
# adfuller test, reject hypothesis = stationary, null = non stationary
# https://www.statsmodels.org/dev/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
# https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html#statsmodels.tsa.stattools.adfuller-returns

def adf_test(timeseries):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)

    return dftest[1]


def kpss_test(timeseries):
    # trend stationary test
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)

    return kpsstest[1]

def check_stationarity(timeseries):
    adf_p = adf_test(timeseries)
    kpss_p = kpss_test(timeseries)

    print('')
    print('Results based on the two tests')
    print('')
    # adf_p < 0.5, reject hypothesis = stationary
    # kpss_p < 0.5, reject hypothesis = non-stationary
    if adf_p < 0.5: 
        if kpss_p < 0.5:
            print('adf concludes STATIONARY, kpss concludes NON-STATIONARY')
            print('The series is difference stationary. Differencing is to be used to make series stationary')
        elif kpss_p >0.5:
            print('adf concludes STATIONARY, kpss concludes STATIONARY')
            print('The series is stationary')
    elif adf_p > 0.5:
        if kpss_p < 0.5:
            print('adf concludes NON-STATIONARY, kpss concludes NON-STATIONARY')
            print('The series is non-stationary')
        elif kpss_p > 0.5:
            print('adf concludes NON-STATIONARY, kpss concludes STATIONARY')
            print('The series is trend stationary. Trend needs to be removed to make series strict stationary. The detrended series is checked for stationarity.')
    return ...



def main():
    set_up_altair()
    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    training_data = incident_count[incident_count['year']<2025]
    test_data = incident_count[incident_count['year']==2025]

    check_stationarity(training_data['Incident'])
    # non-stationary series, but could not use logarithmic transformation as there is 0 in the data. 
    # so change to stl_decompose
    print('finish')


main()