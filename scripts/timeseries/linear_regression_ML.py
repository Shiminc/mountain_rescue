"""
This script runs linear regression using the model from sklearn
fit the model and run evaluation

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import preprocess_data,  aggregate_by_year_month
from utils.features_engineering import create_features
from sklearn.linear_model import LinearRegression
from utils.machine_learning import create_data, run_evaluation, get_predicted_train_test_from_best_model





def main():
    data = preprocess_data()
    incident_count = aggregate_by_year_month(data)
    incident_count.set_index('dateTime', inplace=True)
    
    data = create_features(incident_count)
    
    X_train, X_test, y_train, y_test = create_data(data, 2025)

    model = LinearRegression().fit(X_train, y_train)
    print(f'R2: {model.score}')
    print(model.coef_)
    print(model.intercept_)
    y_test_predict, y_train_predict = get_predicted_train_test_from_best_model(model,X_train, y_train, X_test)

    run_evaluation(y_train, y_test, y_train_predict,y_test_predict)


    print('finish')

main()