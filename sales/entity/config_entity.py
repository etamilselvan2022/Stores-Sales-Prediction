from collections import namedtuple

DataIngestionConfig=namedtuple("DataIngestionConfig",
["train_file_path","test_file_path","raw_data_dir","ingested_train_dir","ingested_test_dir"])


DataValidationConfig=namedtuple("DataValidationConfig",
                                ["schema_file_path","report_file_path","report_page_file_path"])
TrainingPipelineConfig=namedtuple('TrainingPipelineConfig',['artifact_dir'])