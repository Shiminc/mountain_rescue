import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np


def main():
    set_up_altair_browser()
    data = preprocess_data()

    print('finish')

main()