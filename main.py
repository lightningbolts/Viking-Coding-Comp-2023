def timestampToString(timestamp):
    return f"${timestamp / 60}:{timestamp % 60}"


def stringToTimestamp(timeString):
    (hours, minutes) = timeString.split(":")
    return int(hours) * 60 + int(minutes)


def intInput(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid response. Please enter a number.")


def timestampInput(prompt):
    """
    Accepts a time in HH:MM format, 24-hour time.
    :param prompt:
    :return: The time inputted by the user as an integer
    """

    while True:
        try:
            return stringToTimestamp(input(prompt))
        except ValueError:
            print("Invalid response. Please enter a 24-hour time in HH:MM format.")


def rangeInput(prompt):
    print(prompt)
    start = timestampInput("\tEarliest acceptable time: ")
    end = timestampInput("\tLatest acceptable time: ")
    return (start, end)


def main():
    # Introduction: how to use the console application
    # Guidelines
    # Inputs: 
    # number_of_periods_per_day, int
    # length_of_individual_period, int in minutes
    # length_of_break, int in minutes
    # length_of_lunch, int in minutes
    # range_of_lunch_starting_times, [start1, start2]
    # number_of_lunches, int
    # length_of_passing_period, int in minutes
    # range_of_school_starting_times, [start1, start2]
    # range_of_school_ending_times, [end1, end2]
    # misc_name, string
    # misc_duration, int in minutes
    # misc_days, list of days in the week where misc_duration applies
    # Outputs: schedule for the entire week
    number_of_periods_per_day = intInput("How many periods per day? ")
    length_of_individual_period = intInput("How long is each period? ")
    length_of_break = intInput("How long is each break? ")
    length_of_lunch = intInput("How long is lunch? ")
    range_of_lunch_starting_times = rangeInput("When does lunch start? ")
    number_of_lunches = intInput("How many lunches are there? ")
    length_of_passing_period = intInput("How long is each passing period? ")
    range_of_school_starting_times = rangeInput("When does school start? ")
    range_of_school_ending_times = rangeInput("What does school end? ")
    misc_name = input("What is the name of the miscellaneous period? ")
    misc_duration = intInput("How long is the miscellaneous period? ")
    misc_days = input("What days of the week does the miscellaneous period apply? ") # arr of days of the week
    print("The schedule is: ")
    schedule = generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_starting_times, number_of_lunches, length_of_passing_period, range_of_school_starting_times, range_of_school_ending_times, misc_name, misc_duration, misc_days)
    print(schedule)
    
def convert_timestamp_to_minutes_after_midnight(timestamp):
    # timestamp is a string in the format XX:XX (24 hour time)
    return timestamp[0:2] * 60 + timestamp[3:5] # minutes after midnight

def generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_starting_times, number_of_lunches, length_of_passing_period, range_of_school_starting_times, range_of_school_ending_times, misc_name, misc_duration, misc_days):
    return 0

if __name__ == "__main__":
    main()
