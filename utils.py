import functools
import logging
import sys
import os


def create_logger(log_path):
    """Create a logger object with custom handlers. One handler
    sends data to console and another one sends data to logfile.

    Parameters
    ----------
    log_path : str

    Returns
    -------
    logger: logging.Logger
    """

    # create log folder if it doesn't exist
    if not os.path.exists(log_path):
        os.mkdir("logs")

    # create a custom logger
    logger = logging.getLogger(__name__)

    # create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_path)

    console_handler.setLevel(logging.WARNING)
    file_handler.setLevel(logging.ERROR)

    # create formatters and add it to handlers
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# calling the logger
logger = create_logger()


# logfunc
def logfunc(_func=None, logger=logger):
    """A decorator that wraps the passed in function and logs
    exceptions should one occur

    Returns
    -------
    Any
        Output of the inner function 'func'

    Raises
    ------
    Exception of the inner function 'func'
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

                # re-raise the exception
                raise

        return wrapper

    # this ensures that logfunc can be used with or without args
    if _func is None:
        return decorator
    else:
        return decorator(_func)
