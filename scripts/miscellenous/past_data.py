"""
This script runs a quick count with stacked bar chart to show the number of incidents of each cause in the past data gathered. 
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser, create_stacked_bar_by_date, create_histogram
from utils.utils import read_json_to_df, format_time_columns,  convert_to_numeric

from utils.variables import CAUSE_ORDER, PATH_archive
import pandas as pd
import altair as alt
import numpy as np

def main():
    set_up_altair_browser()
    data = read_json_to_df(PATH_archive)
    data = convert_to_numeric(data)
    data = format_time_columns(data)
    create_stacked_bar_by_date(data).show()
    # create_histogram(data).show()
    print('finish')
main()
    