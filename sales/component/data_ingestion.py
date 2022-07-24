from sales.exception import SalesException
from sales.logger import logging
from sales.entity.config_entity import DataIngestionConfig
from sales.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig)-> None:
        try:
            logging.info(f"{'='*30}  Data ingestion log started {'='*30}")
            self.data_ingestion_config=data_ingestion_config
            logging.info(f" data_ingestion_config:\n{data_ingestion_config}")     

        except Exception as e:
            raise SalesException(e,sys) from e

    def download_sales_data(self):
        try:
            train_file_path=self.data_ingestion_config.train_file_path
            test_file_path=self.data_ingestion_config.test_file_path

            train_file_name=os.path.basename(train_file_path)
            test_file_name=os.path.basename(test_file_path)

            raw_data_dir=self.data_ingestion_config.raw_data_dir

            raw_data_train_file_path=os.path.join(raw_data_dir,train_file_name)
            raw_data_test_file_path=os.path.join(raw_data_dir,test_file_name)

            train_data=pd.read_csv(train_file_path)
            test_data=pd.read_csv(test_file_path)

            if train_data is not None:
                os.makedirs(raw_data_dir,exist_ok=True)
                train_data.to_csv(raw_data_train_file_path,index=False)
            if test_data is not None:
                os.makedirs(raw_data_dir,exist_ok=True)
                test_data.to_csv(raw_data_test_file_path,index=False)


            logging.info(f"Data Downloaded Successfully into the path : {raw_data_train_file_path}")

            return raw_data_train_file_path,raw_data_test_file_path   

        except Exception as e:
            raise SalesException(e,sys) from e  

    def split_data_as_train_test(self,train_file_path:str,test_file_path:str):
        try:
            data=pd.read_csv(train_file_path)

            X=data.drop(columns='Item_Outlet_Sales',axis=1)
            y=data['Item_Outlet_Sales'].values

            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

            train_arr=np.c_[X_train,y_train]
            test_arr=np.c_[X_test,y_test]

            train_df=pd.DataFrame(data=train_arr,columns=data.columns)
            test_df=pd.DataFrame(data=test_arr,columns=data.columns)

            train_file_name=os.path.basename(train_file_path)
            test_file_name=os.path.basename(test_file_path)

            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,train_file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,test_file_name)

            if train_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                train_df.to_csv(train_file_path,index=False)

            if test_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                test_df.to_csv(test_file_path,index=False)


            data_ingestion_artifact=DataIngestionArtifact(is_ingested=True, 
                                  message='Data Ingested Successfully', 
                                  train_file_path=train_file_path, 
                                  test_file_path=test_file_path)        

            logging.info(f"data_ingestion_artifact:{data_ingestion_artifact}")
            
            return data_ingestion_artifact
            

        except Exception as e:
            raise SalesException(e,sys) from e              


    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            train_file_path,test_file_path=self.download_sales_data()
            data_ingestion_artifact=self.split_data_as_train_test(train_file_path,test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SalesException(e,sys) from e        

    def __del__(self):
        logging.info(f"{'='*30} Data Ingestion log completed.{'='*30}\n")
