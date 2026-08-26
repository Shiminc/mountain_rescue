"""
This script runs linear regression using the statsmodel as it prints out parameters and diagnostic. 
it supplements the linear regression ran using sklearn
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
from utils.features_engineering import create_features
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from utils.machine_learning import create_data
# performance worse than sarima
# no time lag features
# to avoid using our own forecast as another input for the next forecast (doable but to keep it simple here)
# I am only going to try one lag feature which won't depend on this, that is numbers of previous yeas same month, to run model then predict each month in a year
# I could use time lag say rolling mean of past one year but that means could only forecast next month


def preprocessing_for_statsmodels(data):
    X = pd.get_dummies(data[['count_of_weekend_days','bankholidays','year','month','season','last_year','last_month']],
                            columns = ['season','month'],
                            drop_first = True,
                            dtype = int)

    X_train = X[X['year']<2025]
    X_test = X[X['year']==2025]

    y_train = data[['Incident']][data['year']<2025]
    y_test = data[['Incident']][data['year']==2025]

    return X_train, X_test, y_train, y_test 

def run_ols(X_train, X_test, y_train, y_test):
    # run ols to see how significant each variable is as scikitlearn one won't show this kind of results.
    model = sm.OLS(y_train, X_train)
    result = model.fit()
    print(result.summary())
    residuals = result.resid

    plt.subplot(2,1,1)
    residuals.plot()
    plt.subplot(2,1,2)
    residuals.hist()
    plt.show()

    qqplot(residuals, line='s').show()

    return model

def main():
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    X_train, X_test, y_train, y_test = preprocessing_for_statsmodels(data)
    model = run_ols(X_train, X_test, y_train, y_test)

    
    print('finish')

main()