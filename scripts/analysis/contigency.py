# Run chisquare test for the association between month and incident cause, but unfortunately the assumption not fulfill as some have small values, especially cragfast and others

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser
from utils.utils import preprocess_data,  aggregate_by_year_month, convert_month_to_word,convert_day_to_word
from utils.variables import CAUSE_ORDER 
import pandas as pd
import altair as alt
import numpy as np
from scipy.stats import chisquare
f_exp = np.array([486,318,170,107,135])

def results_heat_map(data):
    data['results'] = data['results'].astype('string')
    data.loc[data['results']=='False','results']='observed lower than expected'
    data.loc[data['results']=='True','results']='observed higher than expected'

    heat_map = alt.Chart(data).mark_rect().encode(
        alt.X('Incident_Cause').sort(CAUSE_ORDER),
        alt.Y('Month:O'),
        alt.Color('results').legend(orient = 'bottom')
    ).properties(
        width=400,
        height=400
    )
    p_value = alt.Chart(data).mark_text(dx=250).encode(
        alt.Y('Month:O'),
        text = alt.Text('p-value')
    )

    observed = alt.Chart(data).mark_text(dy=-7, fontSize=10).encode(
        alt.X('Incident_Cause').sort(CAUSE_ORDER),
        alt.Y('Month:O'),
        text = alt.Text('observed')
    )

    
    expected = alt.Chart(data).mark_text(dy=+3, fontSize=10).encode(
        alt.X('Incident_Cause').sort(CAUSE_ORDER),
        alt.Y('Month:O'),
        text = alt.Text('expected')
    )
    return heat_map + p_value + observed + expected

def create_f_exp(data):
    total_freq = pd.DataFrame(data['Incident_Cause'].value_counts())
    total_freq = total_freq.reset_index()
    # change to category data type so we can sort based on CAUSE_ORDER
    total_freq['Incident_Cause']= total_freq['Incident_Cause'].astype('category')
    total_freq['Incident_Cause'] = total_freq['Incident_Cause'].cat.set_categories(CAUSE_ORDER)
    total_freq = total_freq.sort_values(['Incident_Cause'])
    freq_cause = np.array(total_freq['count'])
    return freq_cause/sum(freq_cause)


def run_chisquare_all_months(df,exp_array, significance=0.05):

    data = df.copy()
    # chisquare_stats = []
    p_value_list = []
    significance_list = []
    # expected_value = []
    month_list = []
    observedHigher = []
    cause_list = []
    observed = []
    expected= []
    for month in range(1,13,1):
        month_df = data.loc[df['month']==month, CAUSE_ORDER]
        print('')
        print('Month ' + str(month))
        print(CAUSE_ORDER)
        observed_list = month_df.values[0]
        print('observed number of incidents')
        print(observed_list)
        expected_list = (exp_array) * sum(observed_list)
        print('expected number of incidents')
        print(np.round(expected_list,decimals=1))
        print('Is observed > expected')
        print(observed_list>expected_list)

        results = chisquare(observed_list,expected_list)
        print('chi-square statistics: ', results.statistic)
        print('p-value: ', results.pvalue)
        print('significance: ', results.pvalue < significance)

        observed = observed + list(observed_list)
        expected = expected + list(np.round(expected_list,decimals=1))
        p_value_list = p_value_list + [np.round(results.pvalue, decimals=3)]*len(CAUSE_ORDER)
        month_list= month_list + [month]*len(CAUSE_ORDER)
        observedHigher= observedHigher + (list(observed_list>expected_list))
        cause_list = cause_list + CAUSE_ORDER

  
    results_for_overview = pd.DataFrame({'Month':month_list, 'Incident_Cause': cause_list, 'observed' : observed, 'expected': expected,'results':observedHigher, 'p-value': p_value_list})
    return results_for_overview

def reorganise_data(data):
    df = pd.DataFrame(data.groupby(['month','Incident_Cause'])['title'].count())
    df = df.reset_index()
    df = df.pivot(index='month',columns = 'Incident_Cause',values='title')
    df = df.reset_index()
    df = df[['month']+CAUSE_ORDER]
    return df

def main():
    set_up_altair_browser()
    data = preprocess_data()
    f_exp = create_f_exp(data)

    df = reorganise_data(data)
    results = run_chisquare_all_months(df, exp_array = f_exp, significance=0.05)

    results_heat_map(results).show()
    print('finish')


main()