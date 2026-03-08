import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import altair as alt
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer

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

def run_grid_search(X_train, y_train, grid_search):
    model = grid_search.fit(X_train, y_train)
    print('print grid_search results')
    print('best params')
    print(model.best_params_)
    print('best_score')
    print(model.best_score_) 
    return model.best_estimator_

def run_evaluation(best_model,X_train, X_test, y_train, y_test):
    y_test_predict = best_model.fit(X_train, y_train).predict(X_test)

    mse_score = mean_squared_error(y_test, y_test_predict)
    mae_score = mean_absolute_error(y_test, y_test_predict)

    print('evaluation based on test data')
    print(f'mse:  {mse_score}')
    print('evaluation based on test data')
    print(f'mae:  {mae_score}')

    y_train_predict = best_model.fit(X_train, y_train).predict(X_train)

    mse_score = mean_squared_error(y_train, y_train_predict)
    mae_score = mean_absolute_error(y_train, y_train_predict)

    print('evaluation based on train data')
    print(f'mse:  {mse_score}')
    print('evaluation based on train data')
    print(f'mae:  {mae_score}')


