import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import datetime 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from sqlalchemy import create_engine


@dataclass

class ConnectDatabase:
    def establish_connection(self, host, user, password, database, tablename):
        self.engine = create_engine(f'mysql://{user}:{password}@{host}/{database}')
        self.tablename = tablename
        print("Table name:", self.tablename)
        print("engine:", self.engine)
        
        
    def retrieve_data(self): 
        data_path = r'C:\Users\Bharath\Desktop\Maddy\third_eye\ML_pipeline\notebooks\data'
        data_path = os.path.join(data_path,'file1.csv')
        print(data_path)
        query = f'SELECT * FROM {self.tablename}'
        print("SQL query:", query)
        df1 = pd.read_sql(query, self.engine)
        df1.to_csv(data_path, index=False, header=True)
        
## Step1: Create path variables to store the files are raw csv

class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

## create a class for Data Ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()

    def get_age(self, age):
        if(age<=18):
            return "Child"
        elif(age>18 and age<=30):
            return "Youth"
        elif(age>30 and age<=40):
            return "Adult"
        elif(age>40 and age<=50):
            return "Mid Age"
        else:
            return "Senior"
    
    def data_cleaning(self, df):
        # self.df = pd.DataFrame(df)
        self.df = df
        # convert transaction col from str to datetime and select hour
        self.df['trans_date_trans_time'] = pd.to_datetime(self.df['trans_date_trans_time']) 
        self.df['time'] = self.df['trans_date_trans_time'].dt.hour
        #drop trans_date
        
        #converting dob to age
        self.df['dob'] = pd.to_datetime(self.df['dob'], dayfirst = True)
        current_date = datetime.datetime.now()
        self.df['age'] = (current_date - self.df['dob']).dt.days // 365
        #drop dob
        
        self.df['age_group'] = self.df['age'].apply(lambda x:self.get_age(x))
        #drop age
        
        self.df = self.df.drop(columns=['trans_date_trans_time','dob','age'],axis=1)
        return self.df
        
    
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods Starts')
        try:
            # mpath = r'C:\Users\Bharath\Desktop\Maddy\third_eye\ML_pipeline\notebooks\data\file1.csv'
            df=pd.read_csv(os.path.join('C:/Users/Bharath/Desktop/Maddy/third_eye/ML_pipeline/notebooks/data','file1.csv'))
            logging.info('Dataset read as pandas Dataframe')

            df = self.data_cleaning(df) 
            
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info('Train test split')
            train_set,test_set=train_test_split(df,test_size=0.20,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of Data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
  
            
        except Exception as e:
            logging.info('Exception occured at Data Ingestion stage')
            raise CustomException(e,sys)
        