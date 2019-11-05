from datetime import datetime
from core import location

import logging
import simplekml


# Initialize logger for the module
logger = logging.getLogger(__name__)


def save_as_gpx(filename, data):
    
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

    except Exception as e:
        logger.error(f'Exception: {str(e)}')


def save_as_kml(filename, data, name="", description=""):
    
    try:
        kml = simplekml.Kml()

        coords=[]
        for loc in data:
            coords.append((loc.latitude, loc.longitude))

        kml.newlinestring(name=name, description=description, coords=coords)

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