import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
from statsmodels.tsa.seasonal import STL as STL
import pandas as pd
import altair as alt

def format_end_time(df):
    df['end_time'] = pd.to_datetime(df['end_time'],format="%H:%M")
    df['start_time'] = pd.to_datetime(df['start_time'],format="%H:%M")

    # to add one day delta to the end time if it ends in the next day
    df['next_day'] = df['end_time'] < df['start_time']   
    # df.loc[df['next_day'] == True,'end_time'] =  df['end_time'] +  pd.Timedelta(days=1)

    for index, row in df.iterrows():
        if row['next_day']:
            # row['end_time'] = row['end_time'] + pd.Timedelta(days=1)
            df.loc[index, 'end_time'] = row['end_time'] + pd.Timedelta(days=1)
            
    # this_is_not_the_df = [row['end_time'] + pd.Timedelta(days=1) for row in df.iterrows() if row['next_day']]
    return df

# TODO add mean/median line 


def gantt_chart(df):
    axis_labels = "datum.label == 0 ? '0 AM' : datum.label == 6 ? '6 AM' : datum.label == 12 ? '12 Noon' : datum.label == 18 ? '6 PM' : datum.label == 24 ? 'Next day' : datum.label == 30 ? '6 AM' : datum.label == 36 ? '12 Noon' : datum.label == 42 ? '6 PM' : datum.label == 48 ? '0 AM' : 'Others'" 
    selection = alt.selection_point(fields=['year'], value=[{'year': 2025}])
    selection_cause = alt.selection_point(fields=['Incident_Cause'], value=[{'Incident_Cause': 'Lost'},
                                                                            {'Incident_Cause': 'Injured & Medical'},
                                                                            {'Incident_Cause': 'Other'},
                                                                            {'Incident_Cause': 'Cragfast'},
                                                                            {'Incident_Cause': 'Overdue'}])
    selection_type = alt.selection_point(fields=['Incident_Type'], value=[{'Incident_Type': 'Full Callout'}, {'Incident_Type': 'Limited Callout'}])
    
    color_year = (
        alt.when(selection)
        # .then(alt.Color('year:N').legend(None))
        .then(alt.value("darkgrey"))
        .otherwise(alt.value("lightgray"))
        )
    
    color_cause = (
        alt.when(selection_cause)
        .then(alt.Color('Incident_Cause:N').legend(None))
        .otherwise(alt.value("lightgray"))
        )
    
    color_type = (
        alt.when(selection_type)
        .then(alt.value("darkgrey"))
        .otherwise(alt.value("lightgray"))
        )
    
    legend_year = alt.Chart(df).mark_rect().encode(
        alt.Y('year:N').axis(title = 'Year', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        # color = alt.Color('year').legend(None)
        color=color_year
    ).add_params(
        selection,
    ).resolve_legend(color = 'independent')


    legend_cause = alt.Chart(df).mark_rect().encode(
        alt.Y('Incident_Cause:N').axis(title = 'Incident Cause', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        # color = alt.Color('year').legend(None)
        color=color_cause
    ).add_params(
        selection_cause,
    ).resolve_legend(color = 'independent')

    legend_type = alt.Chart(df).mark_rect().encode(
        alt.Y('Incident_Type:N').axis(title = 'Incident Type', titleAngle = 0, titleY=-2, titleAlign="left",labelAlign='left', offset=-35,ticks=False, grid=False, domainColor='transparent'),   
        # color = alt.Color('year').legend(None)
        color=color_type
    ).add_params(
        selection_type,
    ).resolve_legend(color = 'independent')


    base = alt.Chart(df).mark_line(size=3,opacity=0.5).encode(
        alt.X('start_hour', axis=alt.Axis(values=[0,6,12,18,24,30,36,42,48], labelExpr=axis_labels), scale = alt.Scale(domain=[0,48])).title(None),
        alt.X2('end_hour').title(None),
        # alt.Y('monthdate(date):T').axis(format='%b').title(None),
        alt.Y('start_hour', axis=alt.Axis(values=[0,6,12,18,24])).sort('ascending').title('Start Time'),
        alt.Tooltip(['Location','Incident_Cause','date','start_time','end_time','hrs','staff']),
        href ='url',
        color = alt.Color('Incident_Cause:N')
    # ).properties(
    #     height = 200,
    #     width = 200
    ).transform_filter(
    # selection & selection_cause 
    selection & selection_cause & selection_type

    )


    next_day_rule = alt.Chart().mark_rule(color='grey',opacity=0.5).encode(
       x=alt.datum(24)
    )

    mean_hours = alt.Chart(df,title=alt.Title('Mean numbers of hours',
                                              anchor='start',
                                            frame='group',
                                            fontSize=12,
       offset=20)).mark_text(xOffset = 50,color='black',fontWeight='bold', fontSize=40).encode(
        text = alt.Text('mean(hrs)',format = '.2')
    ).transform_filter(
    # selection & selection_cause 
    selection & selection_cause & selection_type
    # ).properties(
    #     height = 5
    )

    mean_staff = alt.Chart(df,title=alt.Title('Mean numbers of rescuers',
                                              anchor='start',
                                            frame='group',
                                            fontSize=12,
       offset=20)).mark_text(xOffset = 50,color='black',fontWeight='bold', fontSize=40).encode(
        text = alt.Text('mean(staff)',format = '.2')
    ).transform_filter(
    # selection & selection_cause 
    selection & selection_cause & selection_type
    # ).properties(
    #     height = 5
    )


    next_day = alt.Chart(df,title=alt.Title('Number of overnight operations',
                                              anchor='start',
                                            frame='group',
                                            fontSize=12,
       offset=20)).mark_text(xOffset = 50,color='black',fontWeight='bold', fontSize=40).encode(
        text = alt.Text('sum(next_day)', format='.0f')
    ).transform_filter(
    # selection & selection_cause 
    selection & selection_cause & selection_type
    # ).properties(
    #     height = 5,
    )
    operation_count = alt.Chart(df,title=alt.Title('Number of operations',
                                              anchor='start',
                                            frame='group',
                                            fontSize=12,
       offset=20)).mark_text(xOffset = 50,color='black',fontWeight='bold', fontSize=40).encode(
        text = alt.Text('count(next_day)')
    ).transform_filter(
    # selection & selection_cause 
    selection & selection_cause & selection_type
    # ).properties(
    #     height = 5,

    )
    

    caption =  alt.Chart().mark_text(
        align =  "left",
        baseline = "bottom",
        fontStyle='italic'
    ).encode(

        text = alt.value([
                        'The default shows all Callout incidents in 2025,',
                        'ordered by the start time of the operation',
                        'on the y-axis, and the bar length indicates',
                        'start and end time on the x-axis.',
                        '',
                        'To select a particular incident cause',
                        'or year, click the square beside the label.',
                        'To multi-select, press shift while',
                        'clicking the squares.',
                        'To select all, double click any squares.',
                        '',
                        'You could click on the bar in the chart',
                        'to be brought to the incident report',
                        '',
                        'The mean number of hours and rescuers',
                        'refers to the average number of hours and',
                        'rescuers the selected operations involved', 
                        'not the total (human) hours.',
                        '',
                        'Overnight operations were those that',
                        'went on till the next day.',
                        ])
                          
    )


    calculation = next_day | operation_count | mean_hours | mean_staff
    legend = legend_year| (legend_cause & legend_type)
    
    main = (base + next_day_rule).properties(width=400, height=500)
    return (main| (legend & caption) ) & calculation



# def top_20_hrs(data):
#     year_list = list(data['year'].unique())
#     for i, year in enumerate(year_list):
#         temp_df = data[data['year'] == year]
#         temp_df_top = temp_df.sort_values(by=['hrs'], ascending = False).head(20)
#         if i == 0:
#             df = temp_df_top
#         else:
#             df = pd.concat([df,temp_df_top])

#     return df

def main():
    set_up_altair()
    data = preprocess_data()
        
    # data=top_20_hrs(data)
    chart = gantt_chart(data)
    chart.show()
    chart.save('../../charts/gantt.json')
    chart.save('../../charts/gantt.png')

    print('finish')


main()