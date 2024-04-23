import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_function

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        
    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')
            # Define which columns should be ordinal-encoded and which should be scaled
           
            cat_data=['category','gender','city','lat','job','age_group','time']
            num_data=['amt']
            
            logging.info('Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())
                ]
            )

            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder()),
                'scaler', StandardScaler())
                ]
            )

            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,num_data),
            ('cat_pipeline',cat_pipeline,cat_data)
            ])
            
            return preprocessor

            logging.info('Pipeline Completed')

        except Exception as e:
            logging.info("Error in Data Trnasformation")
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'is_fraud'
            drop_columns = [target_column_name,'Unnamed: 0','cc_num', 'merchant', 'first', 'last','street',
                            'state', 'zip', 'long', 'city_pop', 'trans_num', 'unix_time','merch_lat', 'merch_long']

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            
            ## Transformating using preprocessor obj
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")
    
            target_feature_train_arr = np.array(target_feature_train_df)
            target_feature_test_arr = np.array(target_feature_test_df)

            # train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            # test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_function(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            # return (
            #     train_arr,
            #     test_arr,
            #     self.data_transformation_config.preprocessor_obj_file_path,
            # )
            
            return(
                input_feature_train_arr, target_feature_train_arr,
                input_feature_test_arr, target_feature_test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)