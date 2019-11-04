import json
import os
import logging


# Initialize logger for the module
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
        self.database = None
        self.monitor_frequency = None
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
            self.database = data["database"]
            self.monitor_frequency = data["monitor_frequency"]
            self.recorder_batch_size = data["recorder_batch_size"]
            self.recorder_interval = data["recorder_interval"]

            return 0

        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return -1
