def convert_time_to_seconds(time_str):
    # Split the string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    
    # Convert to total seconds
    total_seconds = minutes * 60 + seconds
    
    # Return the result as a string
    return str(total_seconds)