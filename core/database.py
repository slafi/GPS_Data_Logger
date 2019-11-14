
from datetime import datetime
from core import location

import sqlite3
import os
import logging


# Get the current logger object
logger = logging.getLogger(__name__)


# Initializes the database connection
def check_connection(db_filename, db_path=""):
    """ Checks if it is possible to establish a connection to the SQLite database

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

        return False

    except sqlite3.Error as e:
        logger.error('Database connection error: {0}'.format(e))
        return False

    finally:
        if connection_handler:
            connection_handler.close()


def check_if_datatable_exists(connection_handler, table_name):
    """ Query the database to check if the datatable already exists

        :param connection_handler: the connection handler object
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
        
        return False

    except sqlite3.Error as error:
        logger.error(f"Exception: {str(error)}")
        return False


# Open a new connection handler to the database
def connect(db_filename, db_path=""):

    """ Creates a database connection handler to the SQLite database
        specified by the db_filename parameter

        :param db_filename: database filename
        :param db_path: the path to the database file
        :return: a connection object or None
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

        :param connection_handler: the connection handler object
        :return: 0 if success and -1 if an exception arises
    """

    try:

        if connection_handler is not None:
            connection_handler.close()
        return 0

    except sqlite3.Error as e:
        logger.error('Database disconnection error: {0}'.format(e))
        return -1


def create_location_table(connection_handler, location_table_name="location", session_table_name="session"):

    """ Creates a new SQLite database and a location datatable where the location data will be stored

        :param connection_handler: the Cconnection handler object
        :param table_name: the datatable name
        :return: 0 if succes, -1 if the connection handler is None and -2 if exception arises
    """

    try:
        sql = f"""
                CREATE TABLE IF NOT EXISTS {location_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,                    
                    latitude FLOAT DEFAULT NULL,
                    longitude FLOAT DEFAULT NULL,
                    altitude FLOAT DEFAULT NULL,
                    heading FLOAT DEFAULT NULL,
                    climb FLOAT DEFAULT NULL,
                    speed INTEGER DEFAULT NULL,
                    mode NTEGER DEFAULT 0,
                    utc_time DATETIME DEFAULT NULL,                    
                    db_timestamp DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP)),
                    FOREIGN KEY(session_id) REFERENCES {session_table_name}(id)
                );
               """

        if connection_handler is None:
            return -1

        connection_handler.cursor().execute(sql)
        return 0

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return -2


def create_session_table(connection_handler, session_table_name="session"):

    """ Creates a new SQLite database and session datatable where the session info will be stored

        :param connection_handler: the connection handler object
        :param table_name: the data table name
        :return: 0 if succes, -1 if the connection handler is None and -2 if exception arises
    """

    try:
        sql = f"""
                CREATE TABLE IF NOT EXISTS {session_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,                                       
                    start_timestamp DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP)),
                    end_timestamp DATETIME DEFAULT NULL
                );
               """

        if connection_handler is None:
            return -1

        connection_handler.cursor().execute(sql)
        return 0

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return -2


def get_newest_session_id(connection_handler, session_tablename="session"):

    """
        Returns the latest session identifier
        
        :param connection_handler: the connection handler
        :param session_tablename: the session tablename (default: session)
        :return: latest identifier or 1, -1 if exception is thrown
    """

    try:

        cursor = connection_handler.cursor()
        cursor.execute(f"SELECT max(id) FROM {session_tablename}")
        max_id = cursor.fetchone()[0]

        if max_id is None:
            return 1        # In this case, the session table exists but is empty
        else:
            return max_id

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return -2


def create_new_session(connection_handler, session_tablename="session"):

    """
        Creates a new session record into the session datatable

        :param connection_handler: the connection handler
        :param session_tablename: the session tablename (default: session)
        :return: last inserted row id, -1 if an exception is thrown
    """

    try:
        
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        sql = f"INSERT INTO {session_tablename}(start_timestamp)VALUES(?)"

        cursor = connection_handler.cursor()
        cursor.execute(sql, (timestamp,))

        return cursor.lastrowid

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return -1


def insert_location_data(connection_handler, data, location_table_name="location"):

    """ Query the database to insert a list of location records into the location the database

        :param connection_handler: the connection handler object
        :param data: the list of telemetry records
        :param table_name: the data table name
        :return: count of inserted records or -1 if exception arises
    """

    try:
        cursor = connection_handler.cursor()

        sqlite_insert_query = f"""INSERT INTO `{location_table_name}`
                                ('session_id', 'latitude', 'longitude', 'altitude', 'heading', 'climb', 'speed', 'mode', 'utc_time') 
                                VALUES """

        # condition_if_true if condition else condition_if_false
        for i in range(len(data)):
            item = data[i]

            insert = f"({item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}, '{item[6]}', '{item[7]}', '{item[8]}')"
            sqlite_insert_query = f"{sqlite_insert_query}{insert}"

            if i == len(data)-1:
                sqlite_insert_query = f"{sqlite_insert_query};"
            else:
                sqlite_insert_query = f"{sqlite_insert_query},"

        count = cursor.execute(sqlite_insert_query)
        connection_handler.commit()
        cursor.close()

        logger.debug(f"Data rows inserted: {cursor.rowcount}")
        return count

    except sqlite3.Error as error:
        logger.error(f"Exception: {str(error)}")
        return -1


def retrieve_data(connection_handler, session_id=-1):

    """ Retrieves the location data stored in the database

        :param connection_handler: the connection handler object
        :param session_id: the identifier of the related session
        :return: A list of location objects and None if an exception arises
    """

    try:

        # Check the list of tables
        cursor = connection_handler.cursor()
        if session_id == -1:
            cursor.execute(f"SELECT * FROM location;")
        else:
            cursor.execute(f"SELECT * FROM location WHERE session_id={session_id};")

        rows = cursor.fetchall()

        cursor.close()

        data=[]
        for row in rows:
            loc = location.Location(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            data.append(loc)
        
        return data

    except sqlite3.Error as error:
        logger.error(f"Exception: {str(error)}")
        return None


def update_session_end_timestamp(connection_handler, session_id, session_tablename="session"):

    """ Updates the given session record by setting the end timestamp

        :param connection_handler: the connection handler
        :param session_id: the session identifier
        :param session_tablename: the session tablename (default: session)
        :return: last inserted row id, -1 if an exception is thrown
    """

    try:
        
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        sql = f"UPDATE {session_tablename} SET end_timestamp = '{timestamp}' WHERE id = {session_id}"

        cursor = connection_handler.cursor()
        cursor.execute(sql)
        connection_handler.commit()

        return cursor.lastrowid

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return -1
