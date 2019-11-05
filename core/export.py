from datetime import datetime
from core import location

import simplekml
import logging


# Get the current logger object
logger = logging.getLogger(__name__)


def save_as_gpx(filename, data):
    
    """
        Saves location info retrieved from the database as a GPX file

        :param filename: output GPX filename
        :param data: retrieved location data
        :return: 0 if success and -1 if failure or an exception arises
    """

    try:

        header = f"""<?xml version="1.0" encoding="UTF-8"?>\n""" \
                 f"""<gpx version="1.0">\n"""\
                 f"""<trk><trkseg>\n"""
        footer = f"""</trkseg></trk></gpx>\n"""

        with open(filename, "a+") as outfile:
            
            outfile.write(header)

            for loc in data:
                trk = ''
                if loc.mode == 2:
                    trk = f"""<trkpt lat="{loc.latitude}" lon="{loc.longitude}"><time>{loc.utc_time}</time></trkpt>\n"""
                elif loc.mode == 3:
                    trk = f"""<trkpt lat="{loc.latitude}" lon="{loc.longitude}"><ele>{loc.altitude}</ele><time>{loc.utc_time}</time></trkpt>\n"""
                outfile.write(trk)
            
            outfile.write(footer)

        return 0

    except Exception as e:
        logger.error(f'Exception: {str(e)}')
        return -1


def save_as_kml(filename, data, name="", description=""):

    """
        Saves location info retrieved from the database as a KML file

        :param filename: output KML filename
        :param data: retrieved location data
        :param name: name given to the location data 
        :param description: a description of the location data
        :return: 0 if success and -1 if failure or an exception arises
    """
    
    try:
        kml = simplekml.Kml()

        coords=[]
        for loc in data:
            coords.append((loc.latitude, loc.longitude))

        linestring = kml.newlinestring(name=name, description=description, coords=coords)
        linestring.altitudemode = simplekml.AltitudeMode.relativetoground
        linestring.extrude = 1

        outfile = filename
        n = len(filename)
        ext = filename[n-4:n]
        if(ext.lower() != '.kml'):
            outfile = f"{filename}.kml"

        kml.save(outfile)

        return 0

    except Exception as e:
        logger.error(f'Exception: {str(e)}')
        return -1
