import subprocess
import logging


# Get the current logger object
logger = logging.getLogger(__name__)


class GPSDeviceBinder():

    """ A class to create and release bindings with a BLE device """

    def __init__(self):
        self.stdout_data = None
        self.stderr_data = None

    ## gpsd [-b ] [-D debuglevel] [-F control-socket] [-f framing] [-G ] [-h ] [-l ] [-n ] [-N ] [-P pidfile] [-r ] [-S listener-port] [-s speed] [-V ] [ [source-name] ...]
    ## sudo gpsd -D 4 -F /var/run/gpsd.sock -P /var/run/gpsd.pid -N -n /dev/ttyAMA0
    def bind(self, control_socket="/var/run/gpsd.sock", pid_file="/var/run/gpsd.pid", source_name="/dev/ttyAMA0", debug_level=5, listener_port=2947, sudo=True, timeout=15):
        
        """ Binds the GPSD deamon to a socket file and a device stream.

            :param control_socket: Create a control socket for device addition and removal commands
            :param pid_file: Specify the name and path to record the daemon's process ID
            :param source_name: the GPS device's stream
            :param debug_level: the maximum time period required for the process before it fails
            :param listener_port: Set TCP/IP port on which to listen for GPSD clients (default is 2947)
            :param sudo: a flag indicating if the command is executed with root privileges
            :param timeout: the maximum time period required for the process before it fails
            :return : an integer return code
        """
        if(type(debug_level) is not int):
            return -1
        elif(type(listener_port) is not int):
            return -2
        elif(listener_port > 65535):
            return -3
        else:
            proc = None
            try:
                if sudo:
                    cmd = ['sudo', 'gpsd', '-D', str(debug_level), '-F', str(control_socket), '-P', str(pid_file), '-S', listener_port, '-N', '-n', str(source_name)]
                else:
                    cmd = ['gpsd', '-D', str(debug_level), '-F', str(control_socket), '-P', str(pid_file), '-S', listener_port, '-N', '-n', str(source_name)]

                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                self.stdout_data, self.stderr_data = proc.communicate(timeout)
                return proc.returncode

            except Exception as e:
                logger.error(f'An exception has occured: {str(e)}\n')
                if proc != None:
                    proc.kill()
                self.stdout_data, self.stderr_data = proc.communicate()
                return -4
    

    def release(self):

        """ Removes a current binding with another device.
        """
        pass
