from os import system, name
from datetime import datetime


def clear_console():

    """This function clears the console
    """

    # for windows
    if name == 'nt': 
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')


def get_unix_timestamp():

    """Returns the UNIX timestamp from the current time and date"""
    # current date and time
    now = datetime.now()
    return datetime.timestamp(now)


def get_anterior_datetime(offset = 300):

    """ Returns an anterior date given an offset time in seconds

        :param offset: offset interval in seconds (default: 300s)
        :return datetime: the anterior datetime
        :raises Exception: Invalid time offset
    """

    if offset >= 0:

        now = datetime.now()
        now_ts = datetime.timestamp(now)
        anterior_ts = now_ts - offset

        return datetime.fromtimestamp(anterior_ts)

    else:
        raise Exception("Invalid time offset.")

