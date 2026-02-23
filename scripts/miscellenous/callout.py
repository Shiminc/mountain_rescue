import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
from utils.plot import create_histogram, set_up_altair, create_stacked_bar
import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import ttest_ind

PATH = "../../data/all_incidents.json"
# statistics for incident cause/type for the main variables hrs, total_hrs, staff

def run_chi2(data, cat_a, cat_b):
    table = pd.crosstab(data[cat_a],data[cat_b])
    chi2_res = chi2_contingency(table)
    G_test = chi2_contingency(table, lambda_="log-likelihood")

    print('----')
    print('observation')
    print(pd.crosstab(data[cat_a],data[cat_b], margins=True))
    print('expected frequency')
    print(chi2_res.expected_freq)
    print('degree of freedom')
    print(chi2_res.dof)
    print('chi-square statistic')
    print(chi2_res.statistic)
    print("p-value based on Pearson's chi-squared statistics")
    print(chi2_res.pvalue)
    print('G-test statistic')
    print(G_test.statistic)
    print('p-value based on log-likelihood ratio test')
    print(G_test.pvalue)
    print('----')

    return 

def run_anova(data, ind_var, dep_var):
    # model = ols('hrs ~ C(Incident_Type)', data=data).fit()
    print('Descriptive Statistics')
    print(data.groupby(ind_var)[[dep_var]].agg(['mean', 'std','median','min','max']))

    formula = str(dep_var + '~C(' + ind_var +')')
    model = ols(formula, data=data).fit()
    table = anova_lm(model, typ=2)
    print('----')
    print(table)
    print('')

    print('post-hoc testing (self-correction)')

    for i, factor in enumerate(data[ind_var].unique()):
        if i + 1 < len(data[ind_var].unique()):
            for j in range(i,len(data[ind_var].unique())):
                if factor != data[ind_var].unique()[j]:
                    cat_a = data[data[ind_var]==factor][dep_var]
                    cat_b = data[data[ind_var]==data[ind_var].unique()[j]][dep_var]
                    print('comparing ' + factor + ' and ' + data[ind_var].unique()[j])
                    result = ttest_ind(cat_a, cat_b, equal_var=False)
                    print(result)
                    print('')
    
    print('----')
    return


def main():
    set_up_altair()
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)
    data = data[(data['year']>2014) & (data['year']<2026)]

    # data['Incident_Type'].value_counts()

    print(data.groupby('Incident_Type')[['hrs','staff','total_hrs','Agencies_count','next_day']].agg(['mean', 'median','min','max']))
    print(data.groupby('Incident_Type')[['year','month']].median())


    # (create_histogram(data[data['Incident_Type']=='Alert'],'staff',bin=False) & create_histogram(data[data['Incident_Type']=='Full Callout'],'staff',bin=False) & create_histogram(data[data['Incident_Type']=='Limited Callout'],'staff',bin=False)).show()
    # create_stacked_bar(data, 'Incident_Type', 'Incident_Cause').show()
    run_chi2(data,'Incident_Type','Incident_Cause')
    # run_chi2(data,'Incident_Cause','next_day')
    # run_chi2(data,'Incident_Type','next_day')
    print(' ')

    print('Incident_Type')

    run_anova(data,'Incident_Type','hrs')
    run_anova(data,'Incident_Type','staff')
    run_anova(data,'Incident_Type','total_hrs')

    print('')

    print('Incident_Cause')
    run_anova(data,'Incident_Cause','hrs')
    run_anova(data,'Incident_Cause','staff')
    run_anova(data,'Incident_Cause','total_hrs')

    print('finish')
main()