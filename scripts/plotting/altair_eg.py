import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
import pandas as pd
import altair as alt
from altair import data
import json


set_up_altair()
path='population.json'
with open(path, 'r') as json_file:
        source = json.load(json_file)

source = pd.DataFrame(source)

slider = alt.binding_range(min=1850, max=2000, step=10)
select_year = alt.selection_point(name='year', fields=['year'],
                                   bind=slider, value=2000)

base = alt.Chart(source).add_params(
    select_year
).transform_filter(
    select_year
).transform_calculate(
    gender=alt.expr.if_(alt.datum.sex == 1, 'Male', 'Female')
).properties(
    width=250
)


color_scale = alt.Scale(domain=['Male', 'Female'],
                        range=['#1f77b4', '#e377c2'])

left = base.transform_filter(
    alt.datum.gender == 'Female'
).encode(
    alt.Y('age:O').axis(None),
    alt.X('sum(people):Q')
        .title('population')
        .sort('descending'),
    alt.Color('gender:N')
        .scale(color_scale)
        .legend(None)
).mark_bar().properties(title='Female')

middle = base.encode(
    alt.Y('age:O').axis(None),
    alt.Text('age:Q'),
).mark_text().properties(width=20)

right = base.transform_filter(
    alt.datum.gender == 'Male'
).encode(
    alt.Y('age:O').axis(None),
    alt.X('sum(people):Q').title('population'),
    alt.Color('gender:N').scale(color_scale).legend(None)
).mark_bar().properties(title='Male')

alt.concat(left, middle, right, spacing=5).show()
print('finish')