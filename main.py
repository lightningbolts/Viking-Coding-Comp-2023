import math


def timestampToString(timestamp):
    return f"{math.floor(timestamp / 60)}:{str(timestamp % 60).zfill(2)}"


def stringToTimestamp(timeString):
    (hours, minutes) = timeString.split(":")
    return int(hours) * 60 + int(minutes)


def intInput(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Invalid response. Please enter a positive number.")
            else:
                return value
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
    #There are 1339 minutes in one day, so if the time is more than that, its almost like theres 25 hours in a day
    if start > 1339:
        while start > 1339:
            print("Please keep the time between 0:00 and 23:59")
            start = timestampInput("\tEarliest acceptable time: ")

    end = timestampInput("\tLatest acceptable time: ")
    if end > 1339:
        while end > 1339:
            print("Please keep the time between 0:00 and 23:59")
            end = timestampInput("\tLatest acceptable time: ")

    return tuple([start, end])


def letter(n):
    return chr(ord('A') + n)

def verifyLunch(input, startTime, endTime):
    if(input[0] < startTime or input[-1] < endTime ):
        print("Please make sure lunch starts after school starts or before school ends. ")
        return False
    else:
        return True



class Slot:
    """
    Any scheduled event occupying some period of time (e.g. classes, lunch, breaks, passing periods).
    """

    def __init__(self, name, startTime, length, lunchNum = None):
        self.name = f"{name} {'' if lunchNum is None else f'({letter(lunchNum)})'}"
        self.startTime = startTime
        self.length = length
        self.lunchNum = lunchNum

    def endTime(self):
        return self.startTime + self.length

    def __str__(self):
        return self.name + ": " + timestampToString(self.startTime) + " - " + timestampToString(self.endTime())


class Lunch(Slot):
    pass


class ClassPeriod(Slot):
    def __init__(self, periodNumber, startTime, length, lunchNum = None):
        self.periodNumber = periodNumber
        Slot.__init__(self, f"Period {periodNumber + 1}", startTime, length, lunchNum)

def main():
    print("Bell Schedule Generator")
    print("=" * 20)

    numPeriods = intInput("How many periods are there? ")
    startTime = timestampInput("When does school start? (24-hour time) ")
    latestEndTime = timestampInput("When should school end, at the latest? (24-hour time) ")
    passLen = intInput("How long is each passing period? (minutes) ")
    lunchLen = intInput("How long is lunch? (minutes) ")
    firstLunchStartTimes = rangeInput("When does first lunch start? (24-hour time) ")
    realLunch = verifyLunch(firstLunchStartTimes, startTime, latestEndTime)
    if(realLunch != True):
        firstLunchStartTimes = rangeInput("When does first lunch start? (24-hour time) ")
    numLunches = intInput("How many lunches are there? ")

    '''
    Values for testing
    '''
    '''
    numPeriods = 10
    lunchLen = 30
    firstLunchStartTimes = (stringToTimestamp("11:00"),stringToTimestamp("11:30"))
    numLunches = 2
    passLen = 5
    startTime = stringToTimestamp("8:15")
    latestEndTime = stringToTimestamp("15:15")
    '''

    '''
    Preliminary calculations
    '''
    # numPeriods = 7
    # lunchLen = 30
    # firstLunchStartTimes = (stringToTimestamp("11:00"),stringToTimestamp("11:00"))
    # numLunches = 2
    # passLen = 5
    # startTime = stringToTimestamp("8:15")
    # latestEndTime = stringToTimestamp("15:15")
    
    lunchAndPassLen = lunchLen + passLen
    maxDayLen = latestEndTime - startTime
    try:
        periodLen = math.floor(((maxDayLen - lunchAndPassLen) / numPeriods - passLen))
    except:
        print("There must be at least 1 period.")
        return
    periodAndPassLen = periodLen + passLen
    numPeriodsBeforeLunch = math.floor((firstLunchStartTimes[1] - startTime) / periodAndPassLen)

    firstLunchStartTime = startTime + (numPeriodsBeforeLunch * periodAndPassLen)

    '''
    Errors
    '''
    if periodLen < 0:
        print("Error: There is not enough time in the school day to fit all periods and lunch.")
        return
    if firstLunchStartTime < firstLunchStartTimes[0]:
        print("Error: It is not possible to fit all lunches and have first lunch in the specified timeframe.")
        return


    # The full schedule to be outputted.
    schedule = []

    def addSlot(*args):
        schedule.append(Slot(*args))

    def addClass(*args):
        schedule.append(ClassPeriod(*args))

    # Schedule before lunch, which is the same for everyone
    for i in range(numPeriodsBeforeLunch):
        addClass(i, startTime + i*periodAndPassLen, periodLen)

    # Schedules for each of the different lunches
    for lunchNum in range(numLunches):
        currTime = startTime + numPeriodsBeforeLunch * periodAndPassLen
        if range(numLunches) == 1:
            lunchNum = ""
            break
        else:
            for periodNum in range(numPeriodsBeforeLunch, numPeriodsBeforeLunch + numLunches):
                # If time for lunch
                if periodNum - numPeriodsBeforeLunch == lunchNum:
                    addSlot(f"Lunch", currTime, lunchLen, lunchNum)
                    currTime += lunchAndPassLen

                addClass(periodNum, currTime, periodLen, lunchNum)
                currTime += periodAndPassLen

    # Schedule after all of the lunches, also the same for everyone
    for i in range(numPeriodsBeforeLunch + numLunches, numPeriods):
        addClass(i, startTime + lunchAndPassLen + i*periodAndPassLen, periodLen)
        
    # Loop through the schedule and check to see if any classes with the same period number and different letter go from the same start time to the same end time
    # If so, combine them into one class with the same period number
    # This is done to make the schedule easier to read
    
    for i in range(len(schedule)):
        for j in range(i+1, len(schedule)):
            try:
                if schedule[i].periodNumber == schedule[j].periodNumber and schedule[i].startTime == schedule[j].startTime and schedule[i].endTime() == schedule[j].endTime():
                    schedule[i].name = schedule[i].name[:-3]
                    schedule.pop(j)
            except:
                pass
    
    # Sort the schedule by start time
    schedule.sort(key=lambda slot: slot.startTime)

    # Output the schedule
    print()
    print("Schedule")
    print("="*20)
    print(f"Classes are {periodLen} minutes long")
    print('| {:^20} | {:^5} | {:^5} |'.format("NAME", "START", "END"))
    for slot in schedule:
        if slot.lunchNum is not None:
            pass
        print('| {:^20} | {:>5} | {:>5} |'.format(slot.name, timestampToString(slot.startTime), timestampToString(slot.endTime())))


if __name__ == "__main__":
    main()
