"""
This python file runs an analysis to address the research question
2. Is there any association between the month and the incident cause?
   such that a particular kind of incident occurs more than expected in certain months. 

# Run chisquare test for the frequency of incident cause in each month
# Present the results in a visualisation as well as in print in terminal 


""" 

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair_browser, create_stacked_bar_by_date, create_histogram
from utils.utils import preprocess_data
from utils.variables import CAUSE_ORDER 
import pandas as pd
import altair as alt
import numpy as np
from scipy.stats import chisquare

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

    caption = alt.Chart().mark_text(
        align =  "left",
        baseline = "bottom",).encode(
        text = alt.value(['the p-value for each chisquare conducted for each month is shown',
                         'at the right hand side, while in each square, the number above',
                          'is the observed incident number in the corresponding month and',
                           'incident cause, the number below is the expected frequency based',
                            'on the overall numbers'])
    )
    return (heat_map + p_value + observed + expected) & caption

def create_f_exp(data):
    """
    This function creates the expected frequency for the five incident cause to be used in the chi-square analysis
    This differs from the normal practice of assuming equal sample size as the expected frequency because
    in view of the overwhelmingly more number of some causes in their total count, this is considered more accurate expectancy for each month comparison, else it would be highly like every comparison would be signficant. 
    """
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
    # configure the visualisation
    set_up_altair_browser()
    # read the clean data
    data = preprocess_data()
    # create the expected frequency for the chisquare
    f_exp = create_f_exp(data)
    # reorgnised the data for analysis
    df = reorganise_data(data)
    # run the chisquare for each month and record the data as well as print it out
    results = run_chisquare_all_months(df, exp_array = f_exp, significance=0.05)
    # presented the findings in visualisation
    (results_heat_map(results) | create_stacked_bar_by_date(data, time='month') | create_histogram(data, 'Incident_Cause', bin=False)).show()

    print('finish')


main()