def main():
    # Introduction: how to use the console application
    # Guidelines
    # Inputs: 
    # number_of_periods_per_day, int
    # length_of_individual_period, int in minutes
    # length_of_break, int in minutes
    # length_of_lunch, int in minutes
    # range_of_lunch_starting_times, [min_start_time, max_start_time]
    # number_of_lunches, int
    # length_of_passing_period, int in minutes
    # range_of_school_starting_times, [min_start_time, max_start_time]
    # range_of_school_ending_times, [min_end_time, max_end_time]
    # misc_name, string
    # misc_duration, int in minutes
    # misc_days, list of days in the week where misc_duration applies
    # Outputs: schedule for the entire week
    number_of_periods_per_day = int(input("How many periods per day? "))
    length_of_individual_period = int(input("How long is each period? "))
    length_of_break = int(input("How long is each break? "))
    length_of_lunch = int(input("How long is lunch? "))
    range_of_lunch_starting_times = input("What is the range of lunch starting times? ") # tuple: (min_start_time, max_start_time)
    number_of_lunches = int(input("How many lunches are there? "))
    length_of_passing_period = int(input("How long is each passing period? "))
    school_start_time = input("What is the school starting times? ")
    range_of_school_ending_times = input("What is the range of school ending times? ") # tuple: (min_end_time, max_end_time)
    misc_name = input("What is the name of the miscellaneous period? ")
    misc_duration = int(input("How long is the miscellaneous period? "))
    misc_days = input("What days of the week does the miscellaneous period apply? ") # arr of days of the week
    print("The schedule is: ")
    schedule = generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_starting_times, number_of_lunches, length_of_passing_period, school_start_time, range_of_school_ending_times, misc_name, misc_duration, misc_days)
    print(schedule)
    
def convert_timestamp_to_minutes_after_midnight(timestamp):
    # timestamp is a string in the format XX:XX (24 hour time)
    return timestamp[0:2] * 60 + timestamp[3:5] # minutes after midnight

def iterator(start_time, end_time, increment):
    # start_time and end_time are strings in the format XX:XX (24 hour time)
    # increment is an int in minutes
    # returns a list of timestamps in the format XX:XX (24 hour time)
    start_time = convert_timestamp_to_minutes_after_midnight(start_time)
    end_time = convert_timestamp_to_minutes_after_midnight(end_time)
    timestamps = []
    while start_time < end_time:
        timestamps.append(start_time)
        start_time += increment
    return timestamps

class Period:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return self.name + ": " + self.start_time + " to " + self.end_time

def generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_starting_times, number_of_lunches, length_of_passing_period, school_start_time, range_of_school_ending_times, misc_name, misc_duration, misc_days):
    # Period 1: start_time_of_school to start_time_of_school + length_of_individual_period
    # Break 1: start_time_of_school + length_of_individual_period to start_time_of_school + length_of_individual_period + length_of_break
    
    return 0

if __name__ == "__main__":
    main()
