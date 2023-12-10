import math


def timestampToString(timestamp):
    return f"{math.floor(timestamp / 60)}:{str(timestamp % 60).zfill(2)}"


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
    return tuple([start, end])


def main():
    # Introduction: how to use the console application
    # Guidelines
    # Inputs: 
    # number_of_periods_per_day, int
    # length_of_individual_period, int in minutes
    # length_of_break, int in minutes
    # length_of_lunch, int in minutes
    # range_of_lunch_times, [min_start_time, max_start_time]
    # number_of_lunches, int
    # length_of_passing_period, int in minutes
    # range_of_school_starting_times, [min_start_time, max_start_time]
    # range_of_school_ending_times, [min_end_time, max_end_time]
    # misc_name, string
    # misc_duration, int in minutes
    # misc_days, list of days in the week when misc_duration applies
    # Outputs: schedule for the entire week
    number_of_periods_per_day = intInput("How many periods per day? ")
    length_of_individual_period = intInput("How long is each period? ")
    length_of_break = intInput("How long is each break? ")
    length_of_lunch = intInput("How long is lunch? ")
    range_of_lunch_times = rangeInput("When does lunch start? (24-hour time)")
    number_of_lunches = intInput("How many lunches are there? ")
    length_of_passing_period = intInput("How long is each passing period? ")
    range_of_school_starting_times = rangeInput("When does school start? (24-hour time) ")
    range_of_school_ending_times = rangeInput("What does school end? (24-hour time) ")
    misc_name = input("What is the name of the miscellaneous period? ")
    misc_duration = intInput("How long is the miscellaneous period? ")
    misc_days = input("What days of the week does the miscellaneous period apply? ") # arr of days of the week
    print("The schedule is: ")
    schedule = generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_times, number_of_lunches, length_of_passing_period, range_of_school_starting_times, range_of_school_ending_times, misc_name, misc_duration, misc_days)
    print(schedule)


class Slot:
    """
    Any scheduled event occupying some period of time (e.g. classes, lunch, breaks, passing periods).
    """

    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return self.name + ": " + self.start_time + " - " + self.end_time


def display_schedule(schedule):
    for slot in schedule:
        print(slot)


def generate_schedule(number_of_periods_per_day, length_of_individual_period, length_of_break, length_of_lunch, range_of_lunch_times, number_of_lunches, length_of_passing_period, range_of_school_starting_times, range_of_school_ending_times, misc_name, misc_duration, misc_days):
    result = []
    # Get the amount of time between the start of the school day and the start of lunch
    time_until_lunch = range_of_lunch_times[0] - range_of_school_starting_times[0]
    number_of_periods_before_lunch = math.floor(time_until_lunch / (length_of_individual_period + length_of_passing_period))
    if number_of_periods_before_lunch < 1:
        print("Error: not enough time before lunch to fit all periods")
        return
    # Get the amount of time between the end of lunch and the end of the school day
    time_after_lunch = range_of_school_ending_times[1] - range_of_lunch_times[1]
    number_of_periods_after_lunch = math.floor(time_after_lunch / (length_of_individual_period + length_of_passing_period))
    if number_of_periods_after_lunch < 1:
        print("Error: not enough time after lunch to fit all periods")
        return
    # Add periods before lunch
    for i in range(number_of_periods_before_lunch):
        start_time = range_of_school_starting_times[0] + i * (length_of_individual_period + length_of_passing_period)
        end_time = start_time + length_of_individual_period
        result.append(Slot("Period " + str(i + 1), start_time, end_time))
        
    # Add lunch
    for i in range(number_of_lunches):
        start_time = range_of_lunch_times[0] + i * (length_of_lunch + length_of_passing_period)
        end_time = start_time + length_of_lunch
        result.append(Slot("Lunch " + str(i + 1), start_time, end_time))
    
    # Add periods after lunch
    for i in range(number_of_periods_after_lunch):
        start_time = range_of_lunch_times[1] + i * (length_of_individual_period + length_of_passing_period)
        end_time = start_time + length_of_individual_period
        result.append(Slot("Period " + str(i + 1), start_time, end_time))

    return display_schedule(result)


if __name__ == "__main__":
    # main()
    print(generate_schedule(7, 50, 10, 30, (660, 780), 2, 5, (480, 540), (1020, 1080), "Misc", 30, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]))
