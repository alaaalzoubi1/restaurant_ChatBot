def convert_to_24_hour_manual(time_str):
    # Split the input time string into parts
    parts = time_str.split()


    numeric_part, am_pm = parts[0].lower(), parts[1].lower()

    # Map textual numbers to integers
    number_mapping = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
        'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12
    }

    hour = number_mapping.get(numeric_part, None)
    if hour is not None:
        # Adjust for PM
        if am_pm == 'pm':
            hour += 12
            if hour == 24:
                hour = 12
        elif am_pm == 'am' and hour == 12:
            hour = 0

        return f"{hour:02d}:00:00"
    else:
        return time_str

import re

def is_valid_time_format(time_str):
    # Regular expression pattern for 24-hour time format
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
    return re.match(pattern, time_str) is not None



