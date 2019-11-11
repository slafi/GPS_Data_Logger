

class Location():

    def __init__(self, latitude, longitude, altitude, heading, climb, horizontal_speed, mode, utc_time):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading
        self.climb = climb
        self.horizontal_speed = horizontal_speed
        self.mode = mode
        self.utc_time = utc_time


    def __repr__(self):

        return f"{self.utc_time} [{self.mode}] :: ({self.latitude}, {self.longitude}, {self.altitude}), " \
               f"({self.heading}, {self.horizontal_speed}, {self.heading})"
    