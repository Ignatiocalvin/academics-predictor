# Used to ingest data from a warehouse, database or any other source into the project, usually a job of big data team.
# There a seperate big data team which ensures to get data from various sources and store it in different places like Hadoop, MongoDB etc.
# Data ingestion is the process of loading data from a source system into a data warehouse, data lake or data mart.
# As Data Scientists we need to know how to get data from various sources like hadoop, mongodb, mysql, oracle etc and store it in such a way to make it available for analysis.

import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from functools import reduce
# allow imports when running script from within project dir
# In general, just use sys.path.append() to add to the list of paths from which you can import resource
[sys.path.append(i) for i in ['.', '..']]

# allow imports when running script from project dir parent dirs
l = []
script_path = os.path.split(sys.argv[0])
for i in range(len(script_path)):
  sys.path.append( reduce(os.path.join, script_path[:i+1]) )

# Import modules from other files
from src.components.data_transformation import (DataTransformation,
                                                DataTransformationConfig)
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig
from src.exception import CustomException
from src.logger import logging

# This is a decorator. It is used to add some functionality to the class. If we are defining variables and not
# having functions, then we can use dataclass decorator. It will automatically create the constructor for us.
# By using the @dataclass without using the constructor __init__(), the class (DataTransformationConfig ) 
# accepted the value and assigned to the given variable, so that in this case automatically the 
# 'preprocessor.pkl' file will be created in the 'artifacts' folder.


@dataclass
class DataIngestionConfig:
    '''
    Used for defining the configuration for data ingestion.
    '''
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv') 
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    '''
    Used for ingesting data by making use of the configuration defined in DataIngestionConfig.
    '''
    def __init__(self,ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        self.ingestion_config = ingestion_config
    
    def initiate_data_ingestion(self,raw_data_path: str = None):
        try:
            # Reading data here.
            logging.info("Initiating data ingestion")
            if raw_data_path is not None:
                self.ingestion_config.raw_data_path = raw_data_path
                data = pd.read_csv(self.ingestion_config.raw_data_path)
            else:
                data = pd.read_csv('./assets/data/NewSPerformance.csv')
                        
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            logging.info("Data ingestion completed")
            
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(data,test_size = 0.2, random_state = 18)

            train_set.to_csv(self.ingestion_config.train_data_path,index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path,index = False, header = True)
            logging.info("Train test split ingestion completed")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error("Error occured in data ingestion")
            raise CustomException(e,sys)
    

if __name__ == '__main__':
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation() # We call DataTransformation here, just for the sake of demonstration.
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)
    
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))