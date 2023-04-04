import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(log_path,exist_ok=True)  ## even there is a file , keep on appending files 

LOG_FILE_PATH =  os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    format='[ %(asctime)s ] - %(lineno)d - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO

)

## testing 
# if __name__=="__main__":
#     logging.info("logginfg has started")


## testing custom exception
# if __name__ == "__main__":
#     from exception import Custom_exception
#     import sys 

#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("Division by zero error")
#         raise Custom_exception(e,sys)