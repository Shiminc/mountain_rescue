import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
PATH = "../../data/victims_2021.json"

def create_separate_victims_tuple(df):
    df['human_victims'] = 0
    df['human_victims'] = df['victims'].apply(extract_human_victims)
    df['animal_victims'] = 0
    df['animal_victims'] = df['victims'].apply(extract_animal_victims)
    return df

def extract_human_victims(string):
    stripped_string = string.strip('()')
    string_list = stripped_string.split(',')
    return string_list[0]

def extract_animal_victims(string):
    stripped_string = string.strip('()')
    string_list = stripped_string.split(',')
    return string_list[1]


def main():
    data = read_json_to_df(PATH)
    data = create_separate_victims_tuple(data)
    problem = data[data['human_victims']=='-1']
    print('finish')

main()