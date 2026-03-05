import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import read_json_to_df, format_time_columns, preprocess_data, aggregate_by_year_month, filter_by_year
from utils.plot import set_up_altair
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

PATH = "../../data/all_incidents.json"

def decompose(df):
    # https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.STL.html
    stl_model = STL(df, robust=True)
    # https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.DecomposeResult.html
    return stl_model.fit()

def input_formatting(df):
    """format the input dataframe according to the STL model requirements
        https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.STL.html
    Args:
        path (str): path to input file
        timestamp_col (str): the column for the timestamp of the timeseries
        target_col (str): the column for the target variable

    Returns:
        pd.DataFrame: dataframe with the timestamp to be index
        the panda dataframe that contains 2 columns, including one for timestamp, one for the value,
        assuming only one timeseries.

    TODO:   to handle situation when there are more than one timeseries
    """
    dataframe = df[['dateTime','Incident']]
    # Set the timestamp as index and  target column to y for consistency
    dataframe = dataframe.set_index("dateTime").rename(columns={"Incident": "y"})
    # Only use the 'y' column
    return dataframe[["y"]]


def output_formatting(df, y_var):
    df = df.reset_index().rename(columns={y_var:'Incident'})
    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%d %b %Y')
    return df

def stacked_bar(df):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X('yearmonth(date):T').title(None),
        alt.Y('count()').title(None),
        alt.Color('Incident_Cause')
    )
    return chart


def line_chart(df, series_component, colour='purple', point: bool = False):
    line = alt.Chart(df).mark_line(point=point,color=colour).encode(
        alt.X('dateTime:T').axis(format = "%b %y").title(None),
        alt.Y('Incident:Q').title(series_component),
        tooltip=['yearmonth(dateTime)', 'Incident']
    ).properties(
    width=1000,
    height=100)

    return line

def main():
    set_up_altair()

    # data = read_json_to_df(PATH)
    # data = format_time_columns(data)

    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)
    timeseries = input_formatting(incident_count)
    
    training_data = incident_count[incident_count['year']<2025]
    test_data = incident_count[incident_count['year']==2025]

    # timeseries = input_formatting(training_data)

    decomposed_result = decompose(timeseries)
    trend = pd.DataFrame(decomposed_result.trend)
    seasonal = pd.DataFrame(decomposed_result.seasonal)
    residuals = pd.DataFrame(decomposed_result.resid)

    original_series = output_formatting(timeseries,'y')
    trend = output_formatting(trend,'trend')
    seasonal = output_formatting(seasonal,'season')
    residuals = output_formatting(residuals,'resid')

    ((stacked_bar(data) + line_chart(original_series, 'Observed')) & line_chart(trend, 'trend') & line_chart(seasonal, 'season') & line_chart(residuals, 'residuals')).show()
    # (line_chart(original_series, 'Incident') + line_chart(trend, 'trend')).show()
  
    print('finish')


main()
