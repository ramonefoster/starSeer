class Utils():
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

