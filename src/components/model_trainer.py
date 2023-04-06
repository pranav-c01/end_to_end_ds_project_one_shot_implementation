# here we train different models and then check which of the models is better

import os,sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

## very importnat to include src ke saare modules
par = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(par)

from exception import Custom_exception
from logger import logging
from utils import save_object,evaluate_model

@dataclass  ## no use of init with this decorator  , used to define variables only
class Modeltrainerconfig:
    '''
        inputs given to model trainer component
    '''
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = Modeltrainerconfig()
    
    def initiate_model_trainer(self,train_Arr,test_arr,preprocessor_path):
        try:
            x_train,y_train,x_test,y_test = (
                train_Arr[:,:-1],train_Arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            )
            logging.info("Split training and test input data completed")
            models = {
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boost":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K-Nearest Neighbors":KNeighborsRegressor(),
                "XGBoost":XGBRegressor(),
                "Catboost regresssor":CatBoostRegressor(verbose=False),
                "Adabost regressor":AdaBoostRegressor()
            }

            # evaluate_model is func in utils.py
            model_report = evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            ## To get best model score
            best_model_score = max(model_report.values())

            ## to get best modelname
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise Custom_exception("No best model found")
            logging.info("best model found on both training and testing data")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(x_test)
            r2_sqr = r2_score(y_test,predicted)
            return r2_sqr
        
        except Exception as e:
            Custom_exception(e,sys)
