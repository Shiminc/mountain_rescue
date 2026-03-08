import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import numpy as np
from utils_features import create_features
from sklearn.model_selection import RandomizedSearchCV
from scipy import stats

from xgboost import XGBRegressor
from utils_ML import create_data, run_grid_search, run_evaluation

# https://xgboost.readthedocs.io/en/latest/parameter.html

def create_random_forest_gridsearch():
    """
    Create the gridsearch of the pipeline, for use in the training, as well as later fitting of whole dataset if the
    model is selected for forecasting.

    Returns:
        grid_search model 
    """
    param_grid = {
        "n_estimators": list(range(1, 100)),
        "max_depth": list(range(1, 100)),
        "learning_rate": stats.uniform(0.01, 1),
        "gamma": list(range(1, 100)),
        "colsample_bytree": stats.uniform(0.01, 1),
        "min_child_weight": list(range(1, 100)),
        "subsample": stats.uniform(0.01, 1),
    }

    grid_search = RandomizedSearchCV(XGBRegressor(), param_grid, n_jobs=-1, n_iter=20, cv=10)
    
    return grid_search

def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    grid_search = create_random_forest_gridsearch()

    best_model = run_grid_search(X_train, y_train, grid_search)

    run_evaluation(best_model,X_train, X_test, y_train, y_test)


    print('finish')

main()