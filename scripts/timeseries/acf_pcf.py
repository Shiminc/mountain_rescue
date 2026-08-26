"""
This scripts plot acf and pacf to test for the assumption of time series
# acf :
x = lag
y = correlation coef
colour = confidence level alpha = 0.5
https://www.statsmodels.org/devel/generated/statsmodels.graphics.tsaplots.plot_acf.html#statsmodels.graphics.tsaplots.plot_acf
https://www.statsmodels.org/devel/generated/statsmodels.graphics.tsaplots.plot_pacf.html#statsmodels.graphics.tsaplots.plot_pacf
https://otexts.com/fpp3/acf.html#trend-and-seasonality-in-acf-plots

In time series analysis, the partial autocorrelation function (PACF) gives the partial correlation of a stationary time series with its own lagged values, regressed the values of the time series at all shorter lags. It contrasts with the autocorrelation function, which does not control for other lags.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, month_plot, quarter_plot
from utils.utils import read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
from utils.variables import PATH 
def main():
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

    plot_acf(incident_count['Incident'], lags=48, ax=ax1)
    plot_pacf(incident_count['Incident'], lags = 48, ax=ax2)
    fig.show()
    #null hypothesis is randomness, i.e., stationary
    # results = sm.stats.acorr_ljungbox(incident_count['Incident'])

    # plot_pacf(incident_count['Incident']).show()
    # month_plot(incident_count['Incident']).show()

    print('finish')

main()