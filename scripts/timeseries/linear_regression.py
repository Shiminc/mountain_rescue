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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer

def create_regression_pipeline():
# tranforming data
    numeric_features = ['count_of_weekend_days','bankholidays','year']
    categorical_features = ['month','season']

    preprocessor = ColumnTransformer(
        transformers = [
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )

    regression_pipeline = Pipeline(
        steps = [('preprocessor',preprocessor),
                 ('regressor',LinearRegression())
                 ]
    )

    return regression_pipeline

def create_data(data,year=2025):
    # use 2025 as test data, 2015-2024 as train data
    train_data = data[data['year']<2025]
    test_data = data[data['year'] == 2025]
    
    X_train = train_data[['count_of_weekend_days','bankholidays','year','month','season']]
    y_train = train_data[['Incident']]
    X_test = test_data[['count_of_weekend_days','bankholidays','year','month','season']]
    y_test = test_data[['Incident']]

    return X_train, X_test, y_train, y_test 

def run_scikitlearn_LR( X_train, X_test, y_train, y_test):
    model = create_regression_pipeline()
    model.fit(X_train,y_train)

    mse_score = mean_squared_error(y_test, model.predict(X_test))
    mae_score = mean_absolute_error(y_test, model.predict(X_test))
    print('model score for test data')
    print(f'MSE = {mse_score}')
    print(f'MAE = {mae_score}')


def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)
  
    run_scikitlearn_LR( X_train, X_test, y_train, y_test)

    print('finish')

main()