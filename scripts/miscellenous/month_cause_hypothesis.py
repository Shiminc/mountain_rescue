import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt

def create_proportion_by_cause(data,group_variable):
    agg_data = data.groupby([group_variable,'Incident_Cause'])['Incident'].count().reset_index()
    agg_data.rename(columns={'Incident':'Count'}, inplace = True)
    agg_month = data.groupby([group_variable])['Incident'].count().reset_index()
    agg_month.rename(columns={'Incident':'subtotal'}, inplace = True)
    merged_df = pd.merge(agg_month, agg_data, on = group_variable)
    merged_df['percentage'] = (merged_df['Count']/merged_df['subtotal'])*100
    merged_df.sort_values(by=[group_variable,'percentage'],inplace = True)
   
    return merged_df

def main():
    set_up_altair()
    data = preprocess_data()
    months = create_proportion_by_cause(data,'month')
    years = create_proportion_by_cause(data,'year')

    print('finish')


main()