from utils.utils import handling_problematic_data, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
from utils.plot import set_up_altair
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt
from altair import datum

PATH = "../../data/all_incidents.json"



def trend_year(data):
    df = aggregate_by_year_month(data)
    df = df[df.year>=2015]

    selection = alt.selection_point(fields=['year'], value=[{'year': 2025},{'year':2023},{'year':2024}])
    # selection = alt.selection_point(encodings=['color'], value=[{'year': 2025}], nearest=True, empty=False)
    color = (
        alt.when(selection)
        .then(alt.Color("year:N").scale(scheme="paired").legend(None))
        .otherwise(alt.value("lightgray"))
        )

    legend = alt.Chart(df).mark_rect().encode(
        alt.Y('year:N').axis(title = 'Year', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),        
        color = color
    ).add_params(
        selection,
    ).resolve_legend(color = 'independent')



    chart = alt.Chart(df).mark_line(point=True, size = 5).encode(
        alt.X('month:O'),
        alt.Y('sum(Incident):Q'),
        color = color,
        tooltip=alt.Tooltip(field='year', title=None),

    ).add_params(
        selection,
    )

    month_ave = alt.Chart(df).mark_line(point=True,size=2, color = 'black', strokeDash=[4,2]).encode(
        alt.X('month:O'),
        alt.Y('mean(Incident):Q'),
    )

    return((chart + month_ave).properties(
    width=800,
    height=1000) | legend).configure_legend(False) 


def stacked_bar_chart(data):
    data = data[data.year>= 2015]


    base = alt.Chart(data).encode(
        alt.Y('year:N').axis(None),
        alt.X('count():Q')
    )

    bar_chart = base.mark_bar().encode(
        color = alt.Color('Incident_Cause:N').scale(scheme='tableau10'),
        tooltip = ["Incident_Cause", alt.Text('count()', title=None)]) 
    
    label = base.mark_text(align='left', dx=2).encode(text='count():Q')


    return (bar_chart + label)


def main():
    set_up_altair()

    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = handling_problematic_data(data)

    trend_chart = trend_year(data)
    bar_chart = stacked_bar_chart(data)

    (trend_chart | bar_chart).resolve_scale(color='independent').show()
    print('finish')


main()