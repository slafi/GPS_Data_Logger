from multiprocessing import Queue

# Import custom subpackages
from config import config
from helpers import logger, generic

import os
import sys
import time


# Initialize the logger
logger = logger.get_logger('voltazero_monitor')


if __name__ == '__main__':

    # Clear console
    generic.clear_console()

    logger.info(f'--------------------------------------------------')
    logger.info(f'Main PID: {os.getpid()}')

    # Initialization
    config_file = "./core/config.json"

    # Setup telemetry queue used by the Monitor and Recorder
    q = Queue()

    # Read the application config
    appConfig = config.AppConfig(config_file)
    rc = appConfig.load_app_config()

    if rc == -1:
        logger.error(f'The configuration file cannot be found!')
        sys.exit()
    elif rc == -2:
        logger.error(f'An exception has occured. Application will stop!')
        sys.exit()
    else:
        logger.info(f'App configuration loaded and parsed successfully.')

