import pandas as pd
import json
import time
from datetime import timedelta, date, datetime 
import numpy as np
import altair as alt
import os 

def set_up_altair():
    alt.renderers.enable('browser')
    #alt.renderers.enable('mimetype') # offline renderer
    alt.data_transformers.disable_max_rows()

def create_histogram(df, var_x, bin=True):
    bar_chart = alt.Chart(df).mark_bar().encode(
        alt.X(var_x, bin=bin),
        y = 'count()',
    )
    return bar_chart