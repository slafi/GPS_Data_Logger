
from core import database

from threading import Thread, Event, currentThread

import time
import logging


# Initialize logger for the module
logger = logging.getLogger(__name__)


class Recorder(Thread):

    """ Initiates a connection to the database to store telemetry data
        at regular time intervals

        :param running: an event controlling the process operation
        :param appconfig: the application configuration object
        :param q: the telemetry data queue
        :param id: the recorder thread identifier
        :param enabled: a flag indicating if the monitor is enabled
    """

    def __init__(self, q, appconfig):

        """ Initializes the recorder object

        :param q: the telemetry data queue
        :param appconfig: the application configuration object
        """

        Thread.__init__(self)
        self.running = Event()
        self.id = currentThread().getName()
        self.q = q
        self.appconfig = appconfig
        self.enabled = False


    def init_connection(self):

        """Initializes the database connection"""

        try:
            # Attempt to connect to database (create database if does not already exist)
            self.connection_handler = database.connect(db_filename=self.appconfig.database_filename)

            # If no connection handler, then give up
            if self.connection_handler is None:
                return -1
            else:
                # Create the datatables if they do not already exist
                # Session table
                if not database.check_if_datatable_exists(connection_handler=self.connection_handler, table_name=self.appconfig.session_tablename):
                
                    # Create the session datatable structure
                    database.create_session_table(connection_handler=self.connection_handler, session_table_name=self.appconfig.session_tablename)
                
                # Location table
                if not database.check_if_datatable_exists(connection_handler=self.connection_handler, table_name=self.appconfig.location_tablename):
                
                    # Create the location datatable structure
                    database.create_location_table(connection_handler=self.connection_handler, location_table_name=self.appconfig.location_tablename, session_table_name=self.appconfig.session_tablename)

            return 0

        except Exception as error:
            logger.error(f"Exception: {str(error)}")
            return -2


    def start(self):

        """Starts the recorder thread"""

        self.running.set()
        self.enabled = True
        super(Recorder, self).start()


    def run(self):

        """ Runs the recorder infinite loop """

        # Opens database connection
        rcode = self.init_connection()

        if rcode == 0:

            self.session_id = 1
            if self.appconfig.enable_new_session:
                database.create_new_session(self.connection_handler, session_tablename=self.appconfig.session_tablename)
            
            self.session_id = database.get_newest_session_id(self.connection_handler, session_tablename=self.appconfig.session_tablename)

            # insert data in database
            while (self.running.isSet()):
                self.insert_batch(self.appconfig.recorder_batch_size)
                time.sleep(self.appconfig.recorder_interval)

            # Store the remaning telemetry records in queue before
            # closing connection
            if(self.enabled and not self.q.empty()):
                self.insert_batch(1000)

            # close data connection
            database.disconnect(self.connection_handler)
            
        else:
            logger.error("Failed to initialize database connection")


    def insert_batch(self, size):

        """ Checks if it is possible to establish a connection to the database

        :param size: maximum number of items to save in the database at once
        :return: list of telemetry records to insert in the database
                 if success or None if failure or an exception arises
        """

        try:
            i = 0
            data = []
            while(i < size and not self.q.empty()):
                loc = self.q.get()
                
                arr = []
                if loc.mode == 2:
                    arr = (self.session_id, loc.latitude, loc.longitude, 'NULL', loc.heading, 'NULL', loc.horizontal_speed, loc.mode, loc.utc_time)
                elif loc.mode >= 3:
                    arr = (self.session_id, loc.latitude, loc.longitude, loc.altitude, loc.heading, loc.climb, loc.horizontal_speed, loc.mode, loc.utc_time)

                if arr != []:
                    data.append(arr)
                
                i += 1

            if data != []:
                database.insert_location_data(self.connection_handler, data, location_table_name=self.appconfig.location_tablename)

            logger.debug(f'Current queue size: {self.q.qsize()}')
            return data

        except Exception as inst:
            logger.error(f'Type: {type(inst)} -- Args: {inst.args} -- Instance: {inst}')
            return []


    def stop(self):

        """Stops the recorder thread"""

        self.running.clear()
        self.enabled = False
