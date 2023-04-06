import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer  # used to create a pipeline 
from sklearn.impute import SimpleImputer   ## for missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder

## very importnat to include src ke saare modules
par = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(par)

from exception import Custom_exception
from logger import logging
from utils import save_object
 
@dataclass  ## no use of init with this decorator  , used to define variables only
class DataTransformationconfig:
    '''
        inputs given to data transform component
    '''
    preprocessor_obj_file_path  =  os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationconfig()

    def get_data_transformer_obj(self):
        '''
            This func is responsible for data transformation
        '''
        try:
            numerical_cols = ['reading_score', 'writing_score']
            categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("Numerical columns standard scaling completed")

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Categorical columns encoding completed")

            # combining num and cat pipelines together by column transformer
            preprocessor = ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_cols),  ## doing numerical_pipeline for num columns
                ("cat_pipeline",categorical_pipeline,categorical_cols)  ## doing numerical_pipeline for num columns
                ]
            )

            return preprocessor
        except Exception as e:
            raise Custom_exception(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df =  pd.read_csv(train_path)
            test_df =  pd.read_csv(test_path)
            logging.info("Read train and test data done")

            logging.info("Obtaining Preprocessing object")
            
            preprocessing_obj = self.get_data_transformer_obj()
            target_col_name = "math_score"
            numerical_cols = ['reading_score', 'writing_score']

            ## for train dataset
            input_feature_train_df = train_df.drop(columns=[target_col_name],axis=1)
            target_feature_train_df = train_df[target_col_name]

            ## for test dataset
            input_feature_test_df = test_df.drop(columns=[target_col_name],axis=1)
            target_feature_test_df = test_df[target_col_name]

            logging.info(f"Applying preprocessor object on train and test df.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            ## preparing test and train arr
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
                )

            logging.info("saved preprocessing object")

            return (
                train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise Custom_exception(e,sys)

