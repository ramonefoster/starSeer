
import numpy as np
import math
from starSeer.constants import *

class Utils():
    @staticmethod
    def get_elevation_azimuth(ha, dec, latitude):
        """Calculates Azimuth and Elevation
        params: HourAngle, Declination, Latitude
        return: Elevation, Azimuth
        """ 
        if not Utils.is_numeric(ha):
            ha = Utils.hms_to_hours(ha)
        if not Utils.is_numeric(dec):
            dec = Utils.dms_to_degrees(dec)
        if not Utils.is_numeric(latitude):
            latitude = Utils.dms_to_degrees(latitude)

        H = ha * 15

        #altitude calc
        sinAltitude = (math.sin(dec * DEG2RAD)) * (math.sin(latitude * DEG2RAD)) + (math.cos(dec * DEG2RAD) * math.cos(latitude * DEG2RAD) * math.cos(H * DEG2RAD))
        elevation = math.asin(sinAltitude) * RAD2DEG #altura em graus
        elevation = round(elevation, 2)

        #azimuth calc
        y = -1 * math.sin(H * DEG2RAD)
        x = (math.tan(dec * DEG2RAD) * math.cos(latitude * DEG2RAD)) - (math.cos(H * DEG2RAD) * math.sin(latitude * DEG2RAD))

        #This AZposCalc is the initial AZ for dome positioning
        azimuth = math.atan2(y, x) * RAD2DEG

        #converting neg values to pos
        if (azimuth < 0) :
            azimuth = azimuth + 360    

        return elevation, azimuth
    @staticmethod
    def hours_to_string(hours, decimal_digits=0):
        """
        Converts Float Hour to string Hour, in format hh:mm:ss:cc
        :param hours: Hours (float)
        """
        if not isinstance(hours, (int, float)):
            raise ValueError("Hours must be a number.")
        
        sign = "-" if hours < 0 else "+"
        hours = abs(hours)
        whole_hours = int(hours)
        fractional_hours = hours - whole_hours

        minutes = int(fractional_hours * 60)
        fractional_minutes = fractional_hours * 60 - minutes

        seconds = int(fractional_minutes * 60)
        fractional_seconds = fractional_minutes * 60 - seconds

        seconds_str = f"{seconds:02}.{int(fractional_seconds * (10 ** decimal_digits)):02d}"

        time_string = f"{sign}{whole_hours:02}:{minutes:02}:{seconds_str}"
        
        return time_string

    @staticmethod
    def degrees_to_string(degrees):
        """
        Converts Degrees to string, in format dd:mm:ss:cc
        :param hours: Degrees (float)
        """
        if not isinstance(degrees, (int, float)):
            raise ValueError("Degrees must be a number.")

        sign = "-" if degrees < 0 else "+"
        degrees = abs(degrees)
        degrees_int = int(degrees)
        minutes = int((degrees - degrees_int) * 60)
        seconds = int(((degrees - degrees_int) * 60 - minutes) * 60)
        seconds_decimal = int((((degrees - degrees_int) * 60 - minutes) * 60 - seconds) * 100)

        # Formated value
        degrees_string = f'{sign}{degrees_int:02}:{minutes:02}:{seconds:02}.{seconds_decimal:02}'

        return degrees_string

    @staticmethod
    def hms_to_hours(time_string):
        """
        Converts Hours string to float
        :param time_string: Hours String (hh:mm:ss.ss)
        """        
        # Verify separator
        separators = [':', ' ']
        separator = None
        for sep in separators:
            if sep in time_string:
                separator = sep
                break

        if separator is None:
            raise ValueError("Invalid string format. No recognized separator found.")

        components = time_string.split(separator)

        # Check for correct format
        if len(components) != 3:
            raise ValueError(f"Invalid string format. Expected hh{separator}mm{separator}ss.ss")

        hours = abs(int(components[0]))
        minutes = int(components[1])
        seconds = float(components[2])

        total_hours = hours + minutes / 60 + seconds / 3600

        sign = -1 if "-" in time_string else 1
        return sign*total_hours

    @staticmethod
    def dms_to_degrees(degrees_string):
        """
        Converts Degrees string to float
        :param degrees_string: Degrees String (dd:mm:ss.ss)
        """
        # Verify separator
        separators = [':', ' ']
        separator = None
        for sep in separators:
            if sep in degrees_string:
                separator = sep
                break

        if separator is None:
            raise ValueError("Invalid string format. No recognized separator found.")

        components = degrees_string.split(separator)

        # Check for correct format
        if len(components) != 3:
            raise ValueError("Invalid string format. Expected dd:mm:ss.ss")

        degrees_int = abs(int(components[0]))
        minutes = int(components[1])    
        seconds = float(components[2])

        degrees = degrees_int + minutes / 60 + seconds / 3600

        sign = -1 if "-" in degrees_string else 1
        return sign*degrees

    @staticmethod
    def is_numeric(input):
        """
        Check if the input is a numeric value.
        Parameters:
            input (int or float): The value to be checked.
        Returns:
            bool: True if the input is numeric (int or float), False otherwise.
        """
        if isinstance(input, (int, float)):
            return True
        else:
            return False
    
    @staticmethod
    def check_exists(path):
        """
        Check if a file or directory exists at the given path.
        Parameters:
            path (str): The path to check for existence.
        Returns:
            bool: True if a file or directory exists at the given path, False otherwise.
        """
        import os
        if os.path.exists(path):
            return True
        else:
            return False
    
    @staticmethod
    def add_noise(df, noise_level=0.01):
        noisy_df = df.copy()
        for column in noisy_df.columns:
            if np.issubdtype(noisy_df[column].dtype, np.number):
                noise = np.random.normal(0, noise_level, noisy_df[column].shape)
                noisy_df[column] = noisy_df[column] + noise
        return noisy_df

    @staticmethod
    def check_format(input):
        """
        Check the format of a given input and extract components.

        The expected format is 'x1:x2:x3' or 'x1 x2 x3',
        where 'x1', 'x2', and 'x3' are separated by a colon (':') or a space (' ').

        Parameters:
            input (str): The input to be checked and parsed.

        Returns:
            False: If the input does not match the expected format.
            list: A list containing the three components extracted from the input if the format is correct.
        """
        separators = [':', ' ']
        separator = None
        for sep in separators:
            if sep in input:
                separator = sep
                break

        if separator is None:
            return False

        components = input.split(separator)

        # Check for correct format
        if len(components) != 3:
            return False
        else:
            return components

