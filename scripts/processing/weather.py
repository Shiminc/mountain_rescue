import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt
import json

def main():
    set_up_altair()
    data = preprocess_data()
    data.to_json('full_data.json', orient='records')
    df = data.explode(['Weather'])
    output = df['Weather'].value_counts()
    output = output.to_frame().reset_index().to_json('weather.json',orient='records')
    
    print('finish')



main()