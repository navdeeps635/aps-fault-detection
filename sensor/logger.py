import logging
import os
from datetime import datetime

#log file name
log_file_name = f"{datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.log"

#log directory
log_file_dir = os.path.join(os.getcwd(),"logs")

#create folder if not available
os.makedirs(log_file_dir,exist_ok = True)

#log file path
logging.basicConfig(
    filename = log_file_name,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)