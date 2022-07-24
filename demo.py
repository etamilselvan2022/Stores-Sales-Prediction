from sales.config import Configuration
from sales.exception import SalesException
from sales.component.data_ingestion import DataIngestion
from sales.pipeline import Pipeline

import os,sys
try:
    pipeline=Pipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise SalesException(e,sys) from e
