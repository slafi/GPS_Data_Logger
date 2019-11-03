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
        self.database = None
        self.frequency = None
        self.elm_mac_address = None
        self.use_gps = None
        self.gps_serial_port = None
        self.raw_commands_file = None
        self.supported_commands_file = None
        self.new_session = None

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
            self.database = data["database"]
            self.frequency = data["frequency"]
            self.elm_mac_address = data["elm_mac_address"]
            self.use_gps = data["use_gps"]
            self.gps_serial_port = data["gps_serial_port"]
            self.raw_commands_file = data["raw_commands_file"]
            self.supported_commands_file = data["supported_commands_file"]
            self.new_session = data["new_session"]

            return 0

        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return -1
