from scripts.utils.utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd
import altair as alt

PATH = "../../data/all_incidents.json"

def histogram(df):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X('hrs:Q'),
        alt.Y('count():Q'),
        tooltip=('hrs')
    )
    return chart

def histogram_time(df):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X('end_time:T'),
        alt.Y('count():Q'),
       
    )
    return chart

def main():
    set_up_altair()


    data = read_json_to_df(PATH)
    data['end_time'] = pd.to_datetime(data['end_time'], format = '%H:%M')
    histogram_time(data).show()

    print('finish')


main()