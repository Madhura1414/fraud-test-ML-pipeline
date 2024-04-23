import sys 
import os 
from src.exception import CustomException 
from src.logger import logging 
from src.utils import load_obj
import pandas as pd

class PredictPipeline: 
    def __init__(self) -> None:
        pass

    def predict(self, features): 
        try: 
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join("artifacts", "model.pkl")

            preprocessor = load_obj(preprocessor_path)
            model = load_obj(model_path)

            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e: 
            logging.info("Error occured in predict function in prediction_pipeline location")
            raise CustomException(e,sys)
        
        # 'category', 'amt', 'gender', 'city', 'lat', 'job', 'is_fraud', 'time',
    #    'age_group'
    
    # (['Unnamed: 0', 'trans_date_trans_time', 'cc_num', 'merchant', 'category',
    #    'amt', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip',
    #    'lat', 'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time',
    #    'merch_lat', 'merch_long', 'is_fraud'],
    #   dtype='object')
        
class CustomData: 
        def __init__(self,
                        trans_date_trans_time: str,
                        cc_num:float,
                        merchant:str,
                        category:str,
                        amt:float,
                        first:str,
                        last:str,
                        gender:str,
                        street:str,
                        city:str,
                        state:str,
                        zip:int,
                        lat:float,
                        long:float,
                        city_pop:int,
                        job:str,
                        dob:str,
                        trans_num:str,
                        unix_time:int,
                        merch_lat:float,
                        merch_long:float): 
            self.trans_date_trans_time=trans_date_trans_time
            self.cc_num=cc_num
            self.merchant=merchant
            self.category=category
            self.amt=amt
            self.first=first
            self.last=last
            self.gender=gender
            self.street=street
            self.city=city
            self.state=state
            self.zip=zip
            self.lat=lat
            self.long=long
            self.city_pop=city_pop
            self.job=job
            self.dob=dob
            self.trans_num=trans_num
            self.unix_time=unix_time
            self.merch_lat=merch_lat
            self.merch_long=merch_long
        
        def get_data_as_dataframe(self): 
             try: 
                  custom_data_input_dict = {
                    'trans_date_trans_time':[self.trans_date_trans_time],
                    'cc_num':[self.cc_num],
                    'merchant':[self.merchant],
                    'category':[self.category],
                    'amt':[self.amt],
                    'first':[self.first],
                    'last':[self.last],
                    'gender':[self.gender],
                    'street':[self.street],
                    'city':[self.city],
                    'state':[self.state],
                    'zip':[self.zip],
                    'lat':[self.lat],
                    'long':[self.long],
                    'city_pop':[self.city_pop],
                    'job':[self.job],
                    'dob':[self.dob],
                    'trans_num':[self.trans_num],
                    'unix_time':[self.unix_time],
                    'merch_lat':[self.merch_lat],
                    'merch_long':[self.merch_long]
                  }
                  df = pd.DataFrame(custom_data_input_dict)
                  logging.info("Dataframe created")
                  return df
             except Exception as e:
                  logging.info("Error occured in get_data_as_dataframe function in prediction_pipeline")
                  raise CustomException(e,sys) 
             
             
        