import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
# import altair as alt
import json

def create_season(data):
    data['season'] = "Spring"
    data['order_by_season'] = 0
    data.loc[(data['month']>=3) & (data['month']<=5),'season'] = "Spring"
    data.loc[(data['month']>=3) & (data['month']<=5),'order_by_season'] = 0

    data.loc[(data['month']>=6) & (data['month']<=8),'season'] = "Summer"
    data.loc[(data['month']>=6) & (data['month']<=8),'order_by_season'] = 1

    data.loc[(data['month']>=9) & (data['month']<=11),'season'] = "Autumn"
    data.loc[(data['month']>=9) & (data['month']<=11),'order_by_season'] = 2

    data.loc[(data['month'].isin([12,1,2])),'season'] = "Winter"
    data.loc[(data['month'].isin([12,1,2])),'order_by_season'] = 3

    
    return data.sort_values(by=['order_by_season','month'])

def main():
    data = preprocess_data()
    df = data.groupby(['month','Incident_Cause'])['title'].count().to_frame()
    df.reset_index(inplace = True)
    df.columns = ['month','Incident_Cause','Number_of_Incidents']
    final = df.pivot(
        index = 'month',
        columns ='Incident_Cause',
        values = 'Number_of_Incidents'

    )

    processed_data = create_season(final.reset_index())
    processed_data['month_order']=list(range(0,12))
    processed_data.to_json('month_cause.json', orient='records')

    season_data = processed_data.groupby(['season'])[['Cragfast','Injured & Medical','Lost','Other','Overdue']].sum()
    season_data.reset_index(inplace=True)
    season_melt = pd.melt(
        season_data,
        id_vars = ['season'],
        value_vars = ['Cragfast','Injured & Medical','Lost','Other','Overdue'],
        value_name ='count'
    )
    season_melt.reset_index(drop=True, inplace=True)
    season_melt.sort_values(by=['season','count'],ascending=False,inplace=True)
    season_melt.to_json('season_cause.json',orient='records')
    print('finish')



main()