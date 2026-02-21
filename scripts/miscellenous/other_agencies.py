import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
from utils.plot import set_up_altair, create_histogram, create_stacked_bar
import altair as alt
PATH = "../../data/all_incidents.json"


def create_bar(df):
    chart = alt.Chart()
    return ...

def main():
    variables = ['Incident', 'Incident_Cause', 'Incident_Type', 'url','hrs','staff','total_hrs','year','month',
                 'year_month', 'Other Agencies', 'Agencies_count']
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)

    data = data[data['year']> 2015]

    agencies = data.explode(['Other Agencies'])
    agencies = agencies[variables]
    agencies['Other Agencies'].value_counts()
    set_up_altair()


    # create_histogram(agencies, 'Other Agencies', bin=False).show()
    (create_stacked_bar(agencies, 'Other Agencies', 'Incident_Cause')  
    create_stacked_bar(data, 'Agencies_count', 'Incident_Cause')).show()
    print('finish')
main()