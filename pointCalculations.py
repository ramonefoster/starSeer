import math
from utils import Utils

class Calculations():    
    def __init__(self):
        self.u = Utils()

    def check_instance(self, element):
        return isinstance(element, (int, float))

    def get_elevation_azimuth(self, ha, dec, lat):
        """Calculates Azimuth and Elevation"""
        DEG = 180 / math.pi
        RAD = math.pi / 180.0
        hour_angle = self.u.string_to_hours(ha) * 15 if not self.check_instance(ha) else ha
        declination = self.u.string_to_degrees(dec) if not self.check_instance(dec) else dec
        latitude = self.u.string_to_degrees(lat) if not self.check_instance(lat) else lat        

        #altitude calc
        sinAltitude = (math.sin(declination * RAD)) * (math.sin(latitude * RAD)) + (math.cos(declination * RAD) * math.cos(latitude * RAD) * math.cos(hour_angle * RAD))
        elevation = math.asin(sinAltitude) * DEG #altura em graus
        elevation = round(elevation, 2)

        #azimuth calc
        y = -1 * math.sin(hour_angle * RAD)
        x = (math.tan(declination * RAD) * math.cos(latitude * RAD)) - (math.cos(hour_angle * RAD) * math.sin(latitude * RAD))

        #This AZposCalc is the initial AZ for dome positioning
        azimuth = math.atan2(y, x) * DEG

        #converting neg values to pos
        if (azimuth < 0) :
            azimuth = azimuth + 360    

        return hour_angle, declination, elevation, azimuth


    
