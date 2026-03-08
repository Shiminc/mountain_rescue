import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import numpy as np
from utils_features import create_features
from sklearn.model_selection import RandomizedSearchCV

from sklearn.linear_model import LinearRegression
from utils_ML import create_data, run_grid_search, run_evaluation





def main():
    # set_up_altair()
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    model = LinearRegression().fit(X_train, y_train)
    print(f'R2: {model.score}')
    print(model.coef_)
    print(model.intercept_)
    run_evaluation(model,X_train, X_test, y_train, y_test)


    print('finish')

main()