
from core import location

from threading import Thread, Event, currentThread

import gpsd
import time
import logging


# Initialize logger for the module
logger = logging.getLogger(__name__)


class Monitor(Thread):

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
            
            # Attempts to create a connection to the GPSD server
            gpsd.connect(self.appconfig.gpsd_ip_address, self.appconfig.gpsd_port)

            return 0

        except Exception as error:
            logger.error(f"Exception: {str(error)}")
            return -1


    def start(self):

        """Starts the recorder thread"""

        self.running.set()
        self.enabled = True
        super(Monitor, self).start()


    def run(self):

        """ Runs the recorder infinite loop """

        # Opens database connection
        rcode = self.init_connection()

        if rcode == 0:            

            # insert data in database
            while (self.running.isSet()):
                
                self.report_current_location()                
                time.sleep(self.appconfig.monitor_delay)
            
        else:
            logger.error("Failed to connect to the GPS deamon")


    def report_current_location(self):

        """ Checks if it is possible to establish a connection to the database

        :param size: maximum number of items to save in the database at once
        :return: list of telemetry records to insert in the database
                 if success or None if failure or an exception arises
        """

        try:
            
            # Get current GPS position
            packet = gpsd.get_current()

            # Unpack location parameters
            mode = packet.mode
            latitude = packet.lat
            longitude = packet.lon
            utc_time = packet.time
            track = packet.track
            hspeed = packet.hspeed

            altitude = None
            climb = None
            
            if packet.mode == 3:
                altitude = packet.alt
                climb = packet.climb

            loc = location.Location(latitude=latitude, longitude=longitude, altitude=altitude, heading=track, \
                climb=climb, horizontal_speed=hspeed, mode=mode, utc_time=utc_time)
            
            print(str(loc))         # TODO: remove after DEBUG
            # Put the location instance in the shared queue
            self.q.put(loc)

            return 0

        except Exception as inst:
            logger.error(f'Type: {type(inst)} -- Args: {inst.args} -- Instance: {inst}')
            return -1


    def stop(self):

        """Stops the recorder thread"""

        self.running.clear()

        # disable the monitor
        self.enabled = False
