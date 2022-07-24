from sales.exception import SalesException
from sales.pipeline import Pipeline
import os,sys

try:
    pipeline=Pipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise SalesException(e,sys) from e
