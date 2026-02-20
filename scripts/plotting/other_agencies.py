import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
PATH = "../../data/all_incidents.json"

def main():
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)

    print('finish')
main()