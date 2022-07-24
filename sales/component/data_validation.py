from tkinter import E
from sales.constant import ID_COLUMNS
from sales.exception import SalesException
from sales.logger import logging
import os,sys
from sales.entity.config_entity import DataValidationConfig
from sales.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import pandas as pd
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from sales.util.util import read_yaml_file


class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                      data_ingestion_artifact:DataIngestionArtifact)-> None:
        try:
            logging.info(f"{'='*30} Data Validation log started.{'='*30}\n")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            logging.info(f"data_validation_config  :{data_validation_config}") 
            logging.info(f"data_ingestion_artifact :{data_ingestion_artifact}") 
        except Exception as e:
            raise SalesException(e,sys) from e 


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if train and test file avaiable")
            is_train_file_exist=False
            is_test_file_exist=False

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exist=os.path.exists(test_file_path)

            is_available=is_train_file_exist and is_test_file_exist

            logging.info(f"is train and test file exists ? -> {is_available}")

            if not is_available:
                 train_file_path=self.data_ingestion_artifact.train_file_path
                 test_file_path=self.data_ingestion_artifact.test_file_path
                 message =f"train file {train_file_path} or test file {test_file_path} is not present"
                 raise Exception(message)

            return is_available

        except Exception as e:
            raise SalesException(e,sys) from e    

    
    def  validate_dataset_schema(self)->bool:
        try:
            validation_status=True

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #1. No.of.columns:
            train_data=pd.read_csv(train_file_path)
            test_data=pd.read_csv(test_file_path)

            if train_data.columns.nunique() != test_data.columns.nunique():
                validation_status=False

            #2.Column Names

            for col in train_data.columns.to_list():
                if col not in test_data.columns.to_list():
                    validation_status=False
                    break


            return validation_status

        except Exception as e:
            raise SalesException(e,sys) from e    

    
    def get_train_and_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            id_columns=read_yaml_file(self.data_validation_config.schema_file_path)[ID_COLUMNS]
            return train_df.drop(columns=id_columns,axis=1),test_df.drop(columns=id_columns,axis=1)
        except Exception as e:
            raise SalesException(e,sys) from e 

    def save_data_drift_report_page(self):
        try:
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_and_test_df()

            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir=os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise SalesException(e,sys) from e        

    def get_and_save_data_drift_report(self):
        try:
            profile=Profile(sections=[DataDriftProfileSection()])

            train_df,test_df=self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report=json.loads(profile.json())

            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)

            with open (report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)    

        except Exception as e:
            raise SalesException(e,sys) from e
    
    def is_data_drift_found(self):
        try:
            self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
        except Exception as e:
            raise SalesException(e,sys) from e

    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact=DataValidationArtifact(is_validated=True, message='Data Validated Successfully', 
            schema_file_path=self.data_validation_config.schema_file_path, 
            report_file_path=self.data_validation_config.report_file_path, 
            report_page_file_path=self.data_validation_config.report_page_file_path)

            logging.info(f"data_validation_artifact:{data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SalesException(e,sys) from e


    def __del__(self):
        logging.info(f"\n{'='*30} Data Validation log completed.{'='*30}")
