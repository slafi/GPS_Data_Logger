#!/usr/bin/env python3.7

from multiprocessing import Queue

# Import custom subpackages
from config import config
from helpers import logger, generic
from binders import gps_device_binder
from core import recorder, monitor

import os
import sys
import time


# Initialize the logger
logger = logger.get_logger('gps_locator')


if __name__ == '__main__':

    # Clear console
    generic.clear_console()

    logger.info(f'--------------------------------------------------')
    logger.info(f'Main PID: {os.getpid()}')

    # Initialization
    config_file = "./config/config.json"

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

    # Make sure that the GPSD is launched with the appropriate parameters
    if appConfig.start_gpsd:
        gps_binder = gps_device_binder.GPSDeviceBinder()
        gps_binder.bind(source_name=appConfig.default_device)
        time.sleep(1)

    # Start GPS device monitor
    tmonitor = monitor.Monitor(q, appConfig)
    tmonitor.start()

    # Start database recorder
    # Initialize and start database recorder
    trecorder = recorder.Recorder(q, appConfig)
    trecorder.start()

    try:
        # Sleep main thread
        while True:
            time.sleep(1)

    except Exception as e:
        print(f'Exception: {str(e)}')

    except KeyboardInterrupt:
        logger.info("Stopping all threads and processes... (This may take few seconds)")

        # Stop the monitor process
        tmonitor.stop()
        tmonitor.join()

        # Stop the recorder thread
        trecorder.stop()
        trecorder.join()
