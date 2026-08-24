import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  convert_day_to_word
import pandas as pd


def aggregate_by_week_dayofweek(data):
    # data = convert_day_to_word(data)

    week_day_df = data.groupby(['week_number','year','dayofweek'])['Incident_Cause'].count()
    week_day_df = week_day_df.reset_index()

    frame = create_weeknumber_df()
    df = pd.merge(frame, week_day_df, how='left')
    df.fillna(0,inplace=True)
    df = convert_day_to_word(df)
    df.rename(columns={'Incident_Cause':'Incident_Count'},inplace=True)
    return df.groupby(by=['dayofweek','dayofweek_n'])['Incident_Count'].agg(['count','sum','mean','median','min','max','std'])


def create_weeknumber_df():
    list_pd = []
    for year in range(2015, 2026,1):
        for dayofweek in range(0,7,1):
            for week_number in range(1,53,1):
                list_pd.append({'week_number':week_number,'dayofweek':dayofweek,'year':year})

    return pd.DataFrame(list_pd)

def main():

    set_up_altair_browser()
    data = preprocess_data()
    dayofweek = aggregate_by_week_dayofweek(data)

    print('finish')
main()