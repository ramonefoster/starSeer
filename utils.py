import math

class Utils():
    def hours_to_string(self, hours, decimal_digits=0):
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

    def degrees_to_string(self, degrees):
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

    def string_to_hours(self, time_string):
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

    def string_to_degrees(self, degrees_string):
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

