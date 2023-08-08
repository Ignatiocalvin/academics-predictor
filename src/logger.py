# Logger is for the purpose of logging all the events in the program from execution to termination.
# For example, whenever there is an exception, we can log the exception info in a file via use of logger.

# Read logger documentation at https://docs.python.org/3/library/logging.html
import logging
import os
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs",LOG_FILE_NAME) # This will create logs folder in the same working directory where this file is present
os.makedirs(logs_path,exist_ok=True) # Keep appending the logs in the same directory even if there are multiple runs of the program

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE_NAME)

# Sets the format to be used by the logging module to log the messages.
logging.basicConfig(filename=LOG_FILE_PATH,
                    level=logging.INFO,
                    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s: %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                    ) #This is the change of basic configuration for the logger

if __name__ == '__main__':
    logging.info("This is a test log")
    logging.warning("This is a warning log")
    logging.error("This is an error log")
    logging.critical("This is a critical log")