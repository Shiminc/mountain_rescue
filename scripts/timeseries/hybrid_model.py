import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
import pandas as pd
import numpy as np
from utils_features import create_features
from utils_ML import create_data, run_grid_search, run_evaluation, get_predicted_train_test_from_best_model
from svm import create_svm_gridsearch
from random_forest import create_random_forest_gridsearch
from emsemble import create_xgboost_gridsearch

def run_ml_on_residuals(modelgridsearch, X_train, X_test, y_train, y_test, y_residuals_train, fittedvalue_train_portion, fittedvalue_test_portion):
    print('')
    print(f'run {modelgridsearch} on residuals')
    # run_svm(X_train, X_test, y_residuals_train, y_residuals_test)
    grid_search = modelgridsearch()
    best_model = run_grid_search(X_train, y_residuals_train, grid_search)
    y_test_predict_residual, y_train_predict_residual = get_predicted_train_test_from_best_model(best_model,X_train, y_residuals_train, X_test)

    y_test_predict = fittedvalue_test_portion + y_test_predict_residual
    y_train_predict = fittedvalue_train_portion + y_train_predict_residual

    run_evaluation(y_train, y_test, y_train_predict,y_test_predict)


def main():
    data = preprocess_data()

    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)

    data = create_features(incident_count)
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    # replace y value with residuals from sarima model instead, but dropped 2015 data as the feature engineering (last year) will have to drop the first year data
    residuals = pd.read_pickle('sarima_resid.pkl')
    y_residuals_train = residuals[12:120]
    y_residuals_test = residuals[120:]

    # fitted value from sarima
    fittedvalue = pd.read_pickle('sarima_fitted.pkl')
    # dropped 2015 values as the ml did not predict this first year
    fittedvalue_train_portion = fittedvalue[12:120]
    fittedvalue_test_portion = fittedvalue[120:132]

    run_ml_on_residuals(create_svm_gridsearch, X_train, X_test, y_train, y_test, y_residuals_train, fittedvalue_train_portion, fittedvalue_test_portion)
    run_ml_on_residuals(create_random_forest_gridsearch, X_train, X_test, y_train, y_test, y_residuals_train, fittedvalue_train_portion, fittedvalue_test_portion)
    run_ml_on_residuals(create_xgboost_gridsearch, X_train, X_test, y_train, y_test, y_residuals_train, fittedvalue_train_portion, fittedvalue_test_portion)


    print('finish')

main()