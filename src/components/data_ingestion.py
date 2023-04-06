import os
import sys

# sys.path.append(os.pardir)
# sys.path.append(os.path.join(os.pardir, os.pardir))

## very importnat to include src ke saare modules
par = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
# print(par)
sys.path.append(par)

from exception import Custom_exception
from logger import logging
from data_transformation import DataTransformation
from data_transformation import DataTransformationconfig

from model_trainer import ModelTrainer

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass  ## no use of init with this decorator  , used to define variables only
class Dataingestionconfig:
    '''
        inputs given to data ingestion component
    '''
    train_data_path :str  =  os.path.join("artifacts","train.csv")
    test_data_path :str  =  os.path.join("artifacts","test.csv")
    raw_data_path :str  =  os.path.join("artifacts","data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = Dataingestionconfig()
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info("Read the dataset as df")

            ## crreating artifacts folder and remaining train,set,raw data pathds
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split intiitateed")

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of data completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise Custom_exception(e,sys)


## testing
if __name__ == "__main__":
#     ####### Data ingestion test############
    xd = DataIngestion()
    train_data_path,test_data_path=xd.initiate_data_ingestion()

#     ####### Data transformation test############
    data_transform_obj = DataTransformation()
    train,test,preprocessor_obj_path = data_transform_obj.initiate_data_transformation(train_data_path,test_data_path)

###########  Model trainer.py testing ############
    best_model_initiater = ModelTrainer()
    r2_score = best_model_initiater.initiate_model_trainer(train,test,preprocessor_obj_path)
    print(r2_score)

