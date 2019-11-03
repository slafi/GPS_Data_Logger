from logging import handlers
import logging
import sys


## Create and return a logging object
def get_logger(label, logging_level=logging.DEBUG, enable_console_output=True):

    """This function creates and returns a logging object
        :param label: The label that will be added to the name of the log file 'log_{label}.txt'.
                      The log file is saved by default to the current application path.
        :param logging_level: The logging level (default: DEBUG).
        :param enable_console_output: The boolean flag controlling logging to console (default: True).
    """

    logger = logging.getLogger(label)
    logger.setLevel(logging_level)
    format = logging.Formatter("%(asctime)s [%(relativeCreated)5d - %(name)-5s] [%(levelname)-6s] => %(message)s")

    # Enable logging to console
    if enable_console_output:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        logger.addHandler(ch)

    # Setup file logging
    fh = handlers.RotatingFileHandler('./log_{}.txt'.format(label), maxBytes=(1048576*10), backupCount=7)
    fh.setFormatter(format)
    logger.addHandler(fh)

    return logger