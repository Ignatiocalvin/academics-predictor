# We use this custom exception handling in the project to handle all the errors that will come into the project, simply we can say that we are handling all the errors that will come into the project in a single place.

import sys

# Sys module in python provides various functions and variables that are used to manipulate different parts of the python runtime environment. It allows operating on the python interpreter as it provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
# Read more about sys module here: https://docs.python.org/3/library/sys.html
from src.logger import logging

# The error_detail argument has been passed as sys which is a module in python and has been imported at the top of the code.
# The error_detail argument is used to get the error details.
def error_message_detail(error,error_detail:sys):
    # The error_detail argument is the sys.exc_info() function
    _,_,exec_tb = error_detail.exc_info()
    file_name = exec_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script name {file_name} on line number {exec_tb.tb_lineno} and error is {str(error)}"
    
    return error_message


# This is a custom exception class that inherits from the Exception class in python.
# The Exception class is the base class for all the exceptions in python.
# Read more about Exception class here: https://docs.python.org/3/library/exceptions.html#Exception

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        # The super() function is used to give access to methods and properties of a parent or sibling class.
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail= error_detail)     

    # The __str__ method is a special method that is called when the print() function is invoked on the object. 
    # It must return a string value.
    # When the print() function is called, it calls the __str__ method on the object passed to it and prints the returned value. 
    # If we don't implement the __str__ method for a class, then it will print the default string for the object, which is the object's memory location.
    # Read more about __str__ method here: https://www.educative.io/answers/what-is-the-str-method-in-python
    def __str__(self):
        return f"{self.error_message}"

# Read more about custom exception handling here: https://www.programiz.com/python-programming/user-defined-exception

if __name__ == '__main__':
    try:
        a = 10
        b = 0
        c = a/b
        print(c)
    except Exception as e:
        logging.error(e)
        raise CustomException(e,error_detail=sys)