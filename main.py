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
    number_of_periods_per_day = int(input("How many periods per day? "))
    length_of_individual_period = int(input("How long is each period? "))
    length_of_break = int(input("How long is each break? "))
    length_of_lunch = int(input("How long is lunch? "))
    range_of_lunch_starting_times = input("What is the range of lunch starting times? ") # arr of different times XX:XX
    number_of_lunches = int(input("How many lunches are there? "))
    length_of_passing_period = int(input("How long is each passing period? "))
    range_of_school_starting_times = input("What is the range of school starting times? ") # arr of different times XX:XX
    range_of_school_ending_times = input("What is the range of school ending times? ") # arr of different times XX:XX
    misc_name = input("What is the name of the miscellaneous period? ")
    misc_duration = int(input("How long is the miscellaneous period? "))
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

