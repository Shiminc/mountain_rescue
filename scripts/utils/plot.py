"""
This project used exclusively altair-vega for visualisation https://altair-viz.github.io/index.html
The functions in this module configure the visualisation library output in browsers and jupyter notebook
and create some basic functions for visualisation
"""

import altair as alt

def set_up_altair_browser():
    alt.renderers.enable('browser')
    alt.renderers.set_embed_options(loader={"target": "_blank"})
    #alt.renderers.enable('mimetype') # offline renderer
    alt.data_transformers.disable_max_rows()

def set_up_altair_jupyter():
    alt.renderers.enable('jupyter') # offline renderer


def create_year_month_line_chart(df):
    base = alt.Chart(df).encode(
    x = alt.X('yearmonth(date):T')).configure_view(
    continuousWidth=1200,
    )

    line = base.mark_line().encode(
    y = alt.Y('count():Q'),
    tooltip=alt.Tooltip(['yearmonth(date):T','count():Q'])
    )
    return line

def create_histogram(df, var_x:str, bin=True):
    bar_chart = alt.Chart(df).mark_bar().encode(
        alt.X(var_x, bin=bin),
        alt.Y('count():Q'),
        tooltip=([var_x,'count()'])
    )
    return bar_chart



def create_stacked_bar(df, var_x, stacked_var):
    string_y = 'count(' + stacked_var + ')'
    bar_chart = alt.Chart(df).mark_bar().encode(
        x = var_x,
        y = string_y,
        color = stacked_var
    )

    return bar_chart

def create_stacked_bar_by_date(df,time='year'):
    chart_height = 300

    if time == 'year':
        x_var = 'year(date)'
        chart_width = 600
    elif time == 'yearmonth':
        x_var = 'yearmonth(date)'
        chart_width = 1000
    elif time == 'month':
        x_var = 'month(date)'
        chart_width = 600


    bar_chart = alt.Chart(df).mark_bar().encode(
        x = x_var ,
        y = 'count(Incident_Cause)',
        color = 'Incident_Cause:N'
    ).properties(
        width = chart_width,
        height = chart_height
        )

    return bar_chart