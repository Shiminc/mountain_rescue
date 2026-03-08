import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np
from utils_features import create_features
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from sklearn.metrics import mean_squared_error, mean_absolute_error

# performance worse than sarima
# no time lag features
# to avoid using our own forecast as another input for the next forecast (doable but to keep it simple here)
# I am only going to try one lag feature which won't depend on this, that is numbers of previous yeas same month, to run model then predict each month in a year
# I could use time lag say rolling mean of past one year but that means could only forecast next month



def create_data(data,year=2025):
    # use 2025 as test data, 2015-2024 as train data
    train_data = data[data['year']<2025]
    test_data = data[data['year'] == 2025]
    
    X_train = train_data[['count_of_weekend_days','bankholidays','year','month','season','last_year']]
    y_train = train_data[['Incident']]
    X_test = test_data[['count_of_weekend_days','bankholidays','year','month','season','last_year']]
    y_test = test_data[['Incident']]

    return X_train, X_test, y_train, y_test 


def preprocessing_for_statsmodels(data):
    X = pd.get_dummies(data[['count_of_weekend_days','bankholidays','year','month','season','last_year']],
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

# stats model doesn't work like sklearn
# def run_evaluation(model,X_train, X_test, y_train, y_test):
#     y_test_predict = model.predict(X_test)

#     mse_score = mean_squared_error(y_test, y_test_predict)
#     mae_score = mean_absolute_error(y_test, y_test_predict)

#     print('evaluation based on test data')
#     print(f'mse:  {mse_score}')
#     print('evaluation based on test data')
#     print(f'mae:  {mae_score}')

#     y_train_predict = model.predict(X_train)

#     mse_score = mean_squared_error(y_train, y_train_predict)
#     mae_score = mean_absolute_error(y_train, y_train_predict)

#     print('evaluation based on train data')
#     print(f'mse:  {mse_score}')
#     print('evaluation based on train data')
#     print(f'mae:  {mae_score}')


def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    X_train, X_test, y_train, y_test = preprocessing_for_statsmodels(data)
    model = run_ols(X_train, X_test, y_train, y_test)

    # run_evaluation(model,X_train, X_test, y_train, y_test)
    
    print('finish')

main()