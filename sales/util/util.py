import yaml
from sales.exception import SalesException
import os,sys


def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the content as a dictionary
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SalesException(e,sys) from e




