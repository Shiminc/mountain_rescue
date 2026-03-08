import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import numpy as np
from utils_features import create_features
from sklearn.model_selection import RandomizedSearchCV

from sklearn.svm import SVR
# Epsilon-Support Vector Regression.
from utils_ML import create_data, run_grid_search, run_evaluation



def create_svm_gridsearch():
    """
    Create the gridsearch of the pipeline, for use in the training, as well as later fitting of whole dataset if the
    model is selected for forecasting

    https://scikit-learn.org/1.5/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR

    Returns:
        _type_: _description_
    """
    param_grid = {
        "C": np.logspace(-3,3, 10),
        "gamma": ["scale", "auto", 1, 0.1, 0.01, 0.001, 0.0001],
        "kernel": ['linear', 'poly', 'rbf', 'sigmoid']
    }
    grid_search = RandomizedSearchCV(SVR(), param_grid, n_jobs=-1, n_iter=20, cv=10)
    
    return grid_search

def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    grid_search = create_svm_gridsearch()

    best_model = run_grid_search(X_train, y_train, grid_search)

    run_evaluation(best_model,X_train, X_test, y_train, y_test)


    print('finish')

main()