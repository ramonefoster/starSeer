def convert_hours_to_string(hours, decimal_digits=0):
    sign = '-' if hours < 0 else ''
    abs_hours = abs(hours)
    
    whole_hours = int(abs_hours)
    fractional_hours = abs_hours - whole_hours

    minutes, fractional_minutes = divmod(fractional_hours * 60, 1)
    seconds, fractional_seconds = divmod(fractional_minutes * 60, 1)

    seconds_str = f"{int(seconds):02}.{int(fractional_seconds * (10 ** decimal_digits)):02d}"
    time_string = f"{sign}{whole_hours:02}:{minutes:02}:{seconds_str}"

    return time_string

# Example usage
hours = -12.512638888888888
decimal_digits = 2

time_string = convert_hours_to_string(hours, decimal_digits)
print(time_string)