import json
import os
import logging


# Get the current logger object
logger = logging.getLogger(__name__)


class AppConfig():

    """ This class holdes the application configuration parameters

        :param no_viewer: if a flag indicating whether the viewer should start
    """

    def __init__(self, config_filename):

        """ Initializes the application configuration object

            :param config_filename: configuration filename (and path)
        """

        self.config_filename = config_filename
        self.gpsd_ip_address = None
        self.gpsd_port = None
        self.use_gps = None
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

            # Database parameters
            self.gpsd_ip_address = data["gpsd_ip_address"]
            self.gpsd_port = data["gpsd_port"]
            self.use_gps = data["use_gps"]
            self.enable_new_session = data["enable_new_session"]
            self.database_filename = data["database_filename"]
            self.database = data["database"]
            self.location_tablename = data["location_tablename"]
            self.session_tablename = data["session_tablename"]
            self.monitor_delay = data["monitor_delay"]
            self.recorder_batch_size = data["recorder_batch_size"]
            self.recorder_interval = data["recorder_interval"]

            return 0

        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return -1
