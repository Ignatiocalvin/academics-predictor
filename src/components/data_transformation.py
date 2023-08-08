import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# Defining the paths for the data ingestion
# di_obj = DataIngestion.DataIngestionConfig() # Not required as we already are doing the Doing the addition of paths in data_ingestion.py itself.
# di_obj.train_data_path = "data/train_data.csv"
# di_obj.test_data_path = "data/test_data.csv"

@dataclass #This is a decorator which is used to create a dataclass variables.
class DataTransformationConfig:
    '''
    We are creating a dataclass variable which will be used to store the paths for the data transformation transformer object.
    '''
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    
    def __init__(self,transformation_config: DataTransformationConfig = DataTransformationConfig()):
        self.data_transformation_config = transformation_config

    def get_data_transformer_object(self):
        '''
        This function is responsible for creating a preprocessing data transformation object.
        '''
        try:
            numerical_columns = ["writing_score","reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
                ]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy = 'median')),
                    ("scaler",StandardScaler())
                ]
            )
            
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy = 'most_frequent')),
                    ("one_hot_encoder",OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            
            logging.info(f"Numerical columns:{numerical_columns}")
            logging.info(f"Categorical columns:{categorical_columns}")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)
                ]
            )
            
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        '''
        Here we use the preprocessing object to transform the data.
        '''
            
        try:
            train_df = pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)
            
            
            logging.info("Read train and test data completed") 
            
            logging.info("Obtaining preprocessing object and starting processing.")
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_columns = ["writing_score","reading_score"]
            
            input_feature_train_df = train_df.drop(columns = [target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns = [target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)
            
            # np.c_ is a numpy function that concatenate the columns in the input array
            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
                ]
            
            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
                ]
            
            logging.info(f"Saved Preprocessing object at a particular filepath ")
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
                
        except Exception as e:
            raise CustomException(e,sys)