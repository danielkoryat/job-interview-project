import logging

def error_handler(func):
    #A decorator that wraps the passed in function and logs exceptions.

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the exception with the function name and the error message
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
    return wrapper
