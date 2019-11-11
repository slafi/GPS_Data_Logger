import json
import os
import logging


# Get the current logger object
logger = logging.getLogger(__name__)


class AppConfig():

    """ This class holdes the application configuration parameters

        :param gpsd_ip_address: The GPSD server IP address/hostname (default: '127.0.0.1')
        :param gpsd_port: The GPSD server TCP port (default: 2947)
        :param start_gpsd: A flag indicating if the application should automatically start the GPSD server (default: true)
        :param default_device: The default port to which the USB GPS device is attached  (default: '/dev/ttyACM0')
        :param enable_new_session: A flag indicating that every time the application starts, it creates a new session (default: true)
        :param database_filename: The SQLite database filename and path (default: 'gps_logger.db')
        :param database: The name of the SQLite database (default: 'gps_logger')
        :param session_tablename: The name of the session datatable (default: 'session')
        :param location_tablename: The name of the location datatable      (default: 'location')
        :param monitor_delay: The time interval of the monitor thread (default: 0.5)
        :param recorder_batch_size: The maximum number of data records stored simultaneously in the database (default: 100)
        :param recorder_interval: The time interval of the recorder thread (default: 5)

    """

    def __init__(self, config_filename):

        """ Initializes the application configuration object

            :param config_filename: configuration filename (and path)
        """

        self.config_filename = config_filename
        self.gpsd_ip_address = None
        self.gpsd_port = None
        self.default_device = None
        self.start_gpsd = None
        self.enable_new_session = None
        self.database_filename = None
        self.database = None
        self.session_tablename = None
        self.location_tablename = None
        self.monitor_delay = None
        self.recorder_batch_size = None
        self.recorder_interval = None

    def load_app_config(self):

        """ Attempts to load the application configuration object

            :return: return code if success, -1 if the file does not exist
                     and -2 if an exception arises
        """

        try:

            if not os.path.exists(self.config_filename):
                return -1
            else:
                with open(self.config_filename, 'r') as json_file:
                    data = json.load(json_file)
                    rcode = self.parse_app_config(data)
                    return rcode

        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return -2


    def parse_app_config(self, data):

        """ Attempts to parse the configuration file

            :return: 0 if success, -1 if an exception arises
        """

        try:

            # GPSD / GPS device parameters
            self.gpsd_ip_address = data["gpsd_ip_address"]
            self.gpsd_port = data["gpsd_port"]
            self.start_gpsd = data["start_gpsd"]
            self.default_device = data["default_device"]

            # Database parameters
            self.enable_new_session = data["enable_new_session"]
            self.database_filename = data["database_filename"]
            self.database = data["database"]
            self.location_tablename = data["location_tablename"]
            self.session_tablename = data["session_tablename"]

            # Monitor parameters
            self.monitor_delay = data["monitor_delay"]

            # Recorder parameters
            self.recorder_batch_size = data["recorder_batch_size"]
            self.recorder_interval = data["recorder_interval"]

            return 0

        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return -1
