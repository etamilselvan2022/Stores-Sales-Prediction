import logging
from tkinter import E
from sales.constant import *
from sales.exception import SalesException
import os,sys
from sales.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from sales.util.util import read_yaml_file
from sales.logger import logging


class Configuration:

    def __init__(self,config_file_path:str=CONFIG_FILE_PATH,
                      current_time_stamp=CURRENT_TIME_STAMP)-> None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.timestamp=current_time_stamp
        except Exception as e:
            raise SalesException(e,sys) from e


    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(artifact_dir,
                                                     DATA_INGESTION_ARTIFACT_DIR,
                                                     self.timestamp)
            config_info=self.config_info[DATA_INGESTION_CONFIG_KEY]
            train_file_path=config_info[DATA_INGESTION_TRAIN_FILE_PATH_KEY]
            test_file_path=config_info[DATA_INGESTION_TEST_FILE_PATH_KEY]
            raw_data_dir=os.path.join(data_ingestion_artifact_dir,config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            ingested_dir=os.path.join(data_ingestion_artifact_dir,config_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            ingested_train_dir=os.path.join(ingested_dir,config_info[DATA_INGESTION_TRAIN_DIR_KEY])
            ingested_test_dir=os.path.join(ingested_dir,config_info[DATA_INGESTION_TEST_DIR_KEY])                                         

            data_ingestion_config=DataIngestionConfig(train_file_path=train_file_path, 
                            test_file_path=test_file_path, 
                            raw_data_dir=raw_data_dir, 
                            ingested_train_dir=ingested_train_dir, 
                            ingested_test_dir=ingested_test_dir)

            logging.info(f"data_ingestion_config:{data_ingestion_config}")

            return data_ingestion_config
            
        except Exception as e:
            raise SalesException(e,sys) from e        


    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir,
                                                      DATA_VALIDATION_ARTIFACT_DIR_NAME,
                                                      self.timestamp)
            
            config_info=self.config_info[DATA_VALIDATION_CONFIG_KEY]
            schema_file_path=os.path.join(ROOT_DIR,
                                      config_info[DATA_VALIDATION_SCHEMA_DIR_KEY,
                                      config_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]])

            report_file_path=os.path.join(data_validation_artifact_dir,config_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path=os.path.join(data_validation_artifact_dir,config_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])
                                      
            data_validation_config=DataValidationConfig(schema_file_path=schema_file_path, 
                                 report_file_path=report_file_path, 
                                 report_page_file_path=report_page_file_path)

            logging.info(f"data_validation_config:{data_validation_config}")

            return data_validation_config
            
        except Exception as e:
            raise SalesException(e,sys) from e        

    def get_data_transformation_config(self):
        try:
            pass
        except Exception as e:
            raise SalesException(e,sys) from e   


    def get_model_trainer_config(self):
        try:
            pass
        except Exception as e:
            raise SalesException(e,sys)

    def get_model_evaluation_config(self):
        try:
            pass
        except Exception as e:
            raise SalesException(e,sys) from e

    def get_model_pusher_config(self):
        try:
            pass
        except Exception as e:
            raise SalesException(e,sys) from e  

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            training_pipeline_config_info=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            pipeline_name=training_pipeline_config_info[TRAINING_PIPELINE_NAME_KEY]
            artifact=training_pipeline_config_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            artifact_dir=os.path.join(ROOT_DIR,pipeline_name,artifact)

            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"training_pipeline_config:{training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise SalesException(e,sys) from e                           