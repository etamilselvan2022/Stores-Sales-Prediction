import logging
from datetime import datetime
import os
from sales.constant import *

LOG_DIR='logs'
CURRENT_TIME_STAMP=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
LOG_FILE_NAME=f'log_{CURRENT_TIME_STAMP}.log'

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH=os.path.join(ROOT_DIR,LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
            filemode='w',
            format='[%(asctime)s]^;%(levelname)s^;%(filename)s^;%(funcName)s^;%(lineno)d^;%(message)s',
            level=logging.INFO)



