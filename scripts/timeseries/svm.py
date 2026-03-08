import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np
from features import create_features
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVR
# Epsilon-Support Vector Regression.

def create_data(data,year=2025):
    # use 2025 as test data, 2015-2024 as train data
    train_data = data[data['year']<2025]
    test_data = data[data['year'] == 2025]
    
    X_train = train_data[['count_of_weekend_days','bankholidays','year','month','season','last_year']]
    y_train = train_data[['Incident']]
    X_test = test_data[['count_of_weekend_days','bankholidays','year','month','season','last_year']]
    y_test = test_data[['Incident']]

    preprocessor = transform_features()

    return  preprocessor.fit_transform(X_train),  preprocessor.fit_transform(X_test), np.ravel(y_train), np.ravel(y_test) 


def transform_features():
    # tranforming data
    numeric_features = ['count_of_weekend_days','bankholidays','year']
    categorical_features = ['month','season']

    preprocessor = ColumnTransformer(
        transformers = [
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )

    return preprocessor

def create_svm_gridsearch():
    """
    Create the gridsearch of the pipeline, for use in the training, as well as later fitting of whole dataset if the
    model is selected for forecasting

    https://scikit-learn.org/1.5/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR

    Returns:
        _type_: _description_
    """
    param_grid = {
        "C": np.logspace(-3,3, 5),
        "gamma": ["scale", "auto", 1, 0.1, 0.01, 0.001, 0.0001],
        "kernel": ['linear', 'poly', 'rbf', 'sigmoid']
    }
    grid_search = RandomizedSearchCV(SVR(), param_grid, n_jobs=-1, n_iter=20, cv=10)
    
    return grid_search

def run_grid_search(X_train, y_train, grid_search):
    model = grid_search.fit(X_train, y_train)
    print('print grid_search results')
    print('best params')
    print(model.best_params_)
    print('best_score')
    print(model.best_score_) 
    return model.best_estimator_
  

def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    grid_search = create_svm_gridsearch()

    best_model = run_grid_search(X_train, y_train, grid_search)

    y_predict = best_model.fit(X_train, y_train).predict(X_test)

    mse_score = mean_squared_error(y_test, y_predict)
    mae_score = mean_absolute_error(y_test, y_predict)

    print('evaluation based on test data')
    print(f'mse:  {mse_score}')
    print('evaluation based on test data')
    print(f'mae:  {mae_score}')

    print('finish')

main()