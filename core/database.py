
from datetime import datetime

import sqlite3
import os
import logging


# Initialize logger for the module
logger = logging.getLogger(__name__)


# Initializes the database connection
def check_connection(db_filename, db_path=""):
    """ Checks if it is possible to establish a connection to the database

        :param db_filename: database filename
        :param db_path: the path to the database file
        :return: True if success or False if failure or an exception arises
    """
    try:
        if db_filename is not None:
            db_name = os.path.join(db_path, db_filename)
            connection_handler = connect(db_name)
            if connection_handler is not None:
                return True
            else:
                return False
        else:
            return False

    except sqlite3.Error as e:
        logger.error('Database connection error: {0}'.format(e))
        return False
    finally:
        if connection_handler:
            connection_handler.close()


def check_if_datatable_exists(connection_handler, table_name="data"):
    """ Query the database to check if the data table already eaxists

        :param connection_handler: the Connection object
        :param table_name: the data table name
        :return: True if exists and False if does not exist or exception arises
    """
    try:

        # Check the list of tables
        cursor = connection_handler.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
        list_of_tables = cursor.fetchall()

        cursor.close()

        for item in list_of_tables:
            if table_name == item[0]:
                return True
            else:
                return False

    except sqlite3.Error as error:
        logger.error(f"Exception: {str(error)}")
        return False


# Open a new connection handler to the database
def connect(db_filename, db_path=""):
    """ Creates a database connection handler to the SQLite database
        specified by the db_filename

        :param db_filename: database filename
        :param db_path: the path to the database file
        :return: Connection object or None
    """
    try:
        db_name = os.path.join(db_path, db_filename)
        connection_handler = sqlite3.connect(db_name)
        connection_handler.text_factory = sqlite3.OptimizedUnicode

        return connection_handler
    except sqlite3.Error as e:
        logger.error('Database connection error: {0}'.format(e))
        return None


# Closes the ongoing database connection if still alive
def disconnect(connection_handler):
    """ Closes a current database connection

        :param connection_handler: the Connection object
        :return: 0 if success and -1 if an exception arises
    """
    try:
        if connection_handler is not None:
            connection_handler.close()
        return 0
    except sqlite3.Error as e:
        logger.error('Database disconnection error: {0}'.format(e))
        return -1
