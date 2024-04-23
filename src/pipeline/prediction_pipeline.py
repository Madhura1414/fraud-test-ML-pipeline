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
            data_path = r'C:\Users\Bharath\Desktop\Maddy\third_eye\ML_pipeline\src\pipeline\artifacts'
            preprocessor_path = os.path.join(data_path, 'preprocessor.pkl')
            model_path = os.path.join(data_path, "model.pkl")

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
    

        
class CustomData: 
        def __init__(self,
                        time: str,
                        category:str,
                        amt:float,
                        
                        gender:str,
                        
                        city:str,
                       
                        lat:float,
                       
                        job:str,
                        age_group: str): 
            self.time=time
           
            self.category=category
            self.amt=amt
           
            self.gender=gender
           
            self.city=city
            
            self.lat=lat
            
            self.job=job
            self.age_group = age_group
        
        def get_data_as_dataframe(self): 
             try: 
                  custom_data_input_dict = {
                    'time':[self.time],
                  
                    'category':[self.category],
                    'amt':[self.amt],
                    
                    'gender':[self.gender],
                  
                    'city':[self.city],
                  
                    'lat':[self.lat],
                   
                    'job':[self.job],
                    'age_group':[self.age_group]
                  }
                  df = pd.DataFrame(custom_data_input_dict)
                  logging.info("Dataframe created")
                  return df
             except Exception as e:
                  logging.info("Error occured in get_data_as_dataframe function in prediction_pipeline")
                  raise CustomException(e,sys) 
             
             
        