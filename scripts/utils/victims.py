import pandas as pd
import json, os

def create_separate_victims_tuple(df):
    df['human_victims'] = 0
    df['human_victims'] = df['victims'].apply(extract_human_victims)
    df['animal_victims'] = 0
    df['animal_victims'] = df['victims'].apply(extract_animal_victims)
    return df

def extract_human_victims(string):
    print(string)
    print(type(string))
    stripped_string = string.strip('()')
    string_list = stripped_string.split(',')
    return string_list[0]

def extract_animal_victims(string):
    stripped_string = string.strip('()')
    string_list = stripped_string.split(',')
    return string_list[1]

def create_victims_df():
    path = '../../data/victims'
    file_list = os.listdir(path)
    data_list = []
    for file_path in file_list:
        temp_path = path + '/' + file_path
        with open(temp_path, 'r') as json_file:
            data_list = data_list + json.load(json_file)

    data_pd = pd.DataFrame(data_list)

    return data_pd