import sys
from src.logging.logging import get_logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename 
    
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))
        
if __name__=='__main__':
    logger = get_logger(__name__)
    try:
        logger.info("Enter The Code Block")
        a=1/1
        print("This will not be printed",a)
    except Exception as e:
           raise NetworkSecurityException(e,sys)