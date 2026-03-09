import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import numpy as np
from utils_features import create_features
from sklearn.model_selection import RandomizedSearchCV

from sklearn.ensemble import RandomForestRegressor
from utils_ML import create_data, run_grid_search, run_evaluation, get_predicted_train_test_from_best_model



def create_random_forest_gridsearch():
    """
    Create the gridsearch of the pipeline, for use in the training, as well as later fitting of whole dataset if the
    model is selected for forecasting.

    Returns:
        grid_search model 
    """
    param_grid = {
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor
        "min_samples_leaf": [0.5,1],
        "max_features": [None, "sqrt", "log2"],
        "criterion": [
            "squared_error",
            "poisson",
            "friedman_mse",
            "absolute_error"
        ],
    }

    grid_search = RandomizedSearchCV(RandomForestRegressor(), param_grid, n_jobs=-1, n_iter=20, cv=10)
    
    return grid_search

def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    grid_search = create_random_forest_gridsearch()

    print('')
    print('Random forest on raw data')
    best_model = run_grid_search(X_train, y_train, grid_search)
    y_test_predict, y_train_predict = get_predicted_train_test_from_best_model(best_model,X_train, y_train, X_test)
    run_evaluation(y_train, y_test, y_train_predict,y_test_predict)


    print('finish')

main()