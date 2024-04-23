# from src.components.data_ingestion import ConnectDatabase
from src.components.data_ingestion import ConnectDatabase,DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__": 
    # obj = ConnectDatabase()
    # obj.establish_connection('localhost','root','root123','fraudtest','projectdata')
    # obj.retrieve_data()
    
    obj1 = DataIngestion()
    train_data_path, test_data_path = obj1.initiate_data_ingestion()
    data_transformation = DataTransformation()
    # train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
    # model_trainer = ModelTrainer()
    # model_trainer.initiate_model_training(train_arr, test_arr)
    
    X_train, y_train, X_test, y_test, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
    model_trainer = ModelTrainer()
    model_trainer.initiate_model_training(X_train, y_train, X_test, y_test)

#