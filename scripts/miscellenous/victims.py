import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.victims import create_separate_victims_tuple, create_victims_df
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
from utils.plot import create_histogram, set_up_altair, create_stacked_bar
import pandas as pd
PATH = "../../data/all_incidents.json"


def main():
    set_up_altair()
    victim = create_victims_df()
    victim = create_separate_victims_tuple(victim)
    victim = victim[['Incident','human_victims']]

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)
    data = data[(data['year']>2020) & (data['year']<2026)]

    data_merged = pd.merge(data, victim, how = 'left', on = 'Incident')
    data_merged['ratio'] = data_merged['staff']/data_merged['human_victims']

    # create_histogram(data_merged, 'ratio', False).show()
    create_stacked_bar(data_merged, 'ratio', 'Incident_Cause').show()
    print('pause')

    print('finish')

main()