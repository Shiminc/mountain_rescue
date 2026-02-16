from scripts.utils.utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd
import altair as alt

PATH = "../../data/all_incidents.json"

def line_chart(df):
    line_chart = alt.Chart(df).mark_line().encode(
        alt.X('month:O'),
        alt.Y('value:Q'),
        alt.Color('variable:O')  
    ).properties(
    width=600,
    height=100)
    return line_chart

def aggregate_by_month(df):
    aggregated_df = df.pivot_table(index=['month'],
                              #columns='Incident_Type',
                              values='Incident',
                              aggfunc='mean', 
                              fill_value=0)
                              #margins=True
    return aggregated_df

def main():
    set_up_altair()

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    incident_count = aggregate_by_year_month(data)
    previous_years = incident_count[incident_count['year'] < 2025]
    current_year =  incident_count[(incident_count['year'] == 2025)]
    current_year = current_year[['month','Incident']].rename(columns={"Incident":"2025"})
    aggregated_month = aggregate_by_month(incident_count).reset_index().rename(columns={"Incident":"Average_in_past_years"})
    
    merged_df = pd.merge(aggregated_month, current_year, how = 'left')
    merged_df = pd.melt(merged_df, id_vars = ['month'], value_vars=['Average_in_past_years', '2025'])
    line_chart(merged_df).show()
    print('finish')


main()