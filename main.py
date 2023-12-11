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
    # There are 1339 minutes in one day, so if the time is more than that, its almost like there's 25 hours in a day
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


class Slot:
    """
    Any scheduled event occupying some period of time (e.g. classes, lunch, breaks, passing periods).
    """

    def __init__(self, name, startTime, length, lunchNum=None):
        self.name = f"{name} {'' if lunchNum is None else f'({letter(lunchNum)})'}"
        self.startTime = startTime
        self.length = length
        self.lunchNum = lunchNum

    def endTime(self):
        return self.startTime + self.length

    def __str__(self):
        return self.name + ": " + timestampToString(self.startTime) + " - " + timestampToString(self.endTime())


class ClassPeriod(Slot):
    def __init__(self, periodNumber, startTime, length, lunchNum=None):
        self.periodNumber = periodNumber
        Slot.__init__(self, f"Period {periodNumber + 1}", startTime, length, lunchNum)


class InvalidSchedule(Exception):
    pass


def main():
    print("Bell Schedule Generator")
    print("=" * 20)

    numPeriods = intInput("How many periods are there? ")
    startTime = timestampInput("When does school start? (24-hour time) ")
    latestEndTime = timestampInput("When should school end, at the latest? (24-hour time) ")
    if latestEndTime < startTime:
        while latestEndTime < startTime:
            print("Error: School can't start before it ends. ")
            startTime = timestampInput("When does school start? (24-hour time) ")
            latestEndTime = timestampInput("When should school end, at the latest? (24-hour time) ")


    passLen = intInput("How long is each passing period? (minutes) ")
    if passLen == 0:
        while passLen == 0:
            print("Error: Passing periods must be longer than 0 minutes. ")
            passLen = intInput("How long is each passing period? (minutes) ")

    lunchLen = intInput("How long is lunch? (minutes) ")
    while True:
        firstLunchStartTimes = rangeInput("When does first lunch start? (24-hour time) ")
        if firstLunchStartTimes[0] < startTime or firstLunchStartTimes[-1] > latestEndTime:
            print("Please make sure lunch starts after school starts or before school ends. ")
        break
    numLunches = intInput("How many lunches are there? ")

    try:
        printSchedule(
            *scheduler(numPeriods, startTime, latestEndTime, passLen, lunchLen, firstLunchStartTimes, numLunches))
    except InvalidSchedule:
        print()


def scheduler(numPeriods, startTime, latestEndTime, passLen, lunchLen, firstLunchStartTimes, numLunches):
    """
    :param numPeriods:
    :param startTime:
    :param latestEndTime:
    :param passLen:
    :param lunchLen:
    :param firstLunchStartTimes:
    :param numLunches:
    :return:
    """

    lunchAndPassLen = lunchLen + passLen
    maxDayLen = latestEndTime - startTime
    periodLen = math.floor(((maxDayLen - lunchAndPassLen) / numPeriods - passLen))

    periodAndPassLen = periodLen + passLen
    numPeriodsBeforeLunch = math.floor((firstLunchStartTimes[1] - startTime) / periodAndPassLen)
    firstLunchStartTime = startTime + (numPeriodsBeforeLunch * periodAndPassLen)
    schedule = []

<<<<<<< HEAD
    '''
    Errors
    '''

=======
>>>>>>> 649b2f37bd98f3bd7b67b30f603e30c0904bb9f9
    if periodLen < 0:
        print("Error: There is not enough time in the school day to fit all periods and lunch.")
        raise InvalidSchedule
    if firstLunchStartTime < firstLunchStartTimes[0]:
        print("Error: It is not possible to fit all lunches and have first lunch in the specified timeframe.")
        raise InvalidSchedule

    def addSlot(*args):
        schedule.append(Slot(*args))

    def addClass(*args):
        schedule.append(ClassPeriod(*args))

    # Schedule before lunch, which is the same for everyone
    for i in range(numPeriodsBeforeLunch):
        addClass(i, startTime + i * periodAndPassLen, periodLen)

    # Schedules for each of the different lunches
    for lunchNum in range(numLunches):
        currTime = startTime + numPeriodsBeforeLunch * periodAndPassLen
        effectiveLunchNum = None if numLunches == 1 else lunchNum
        for periodNum in range(numPeriodsBeforeLunch, numPeriodsBeforeLunch + numLunches):
            # If time for lunch
            if periodNum - numPeriodsBeforeLunch == lunchNum:
                addSlot(f"Lunch", currTime, lunchLen, effectiveLunchNum)
                currTime += lunchAndPassLen

            if periodNum < numPeriodsBeforeLunch + numLunches - 1:
                addClass(periodNum, currTime, periodLen, effectiveLunchNum)
                currTime += periodAndPassLen

    # Schedule after all the lunches, also the same for everyone
    for i in range(numPeriodsBeforeLunch + numLunches - 1, numPeriods):
        addClass(i, startTime + lunchAndPassLen + i * periodAndPassLen, periodLen)

    schedule.sort(key=lambda slot: slot.startTime)

    # Sort the schedule by start time
    return periodLen, schedule


def printSchedule(periodLen, schedule):
    print()
    print("Schedule")
    print("=" * 20)
    print(f"Classes are {periodLen} minutes long")
    print('| {:^20} | {:^5} | {:^5} |'.format("NAME", "START", "END"))
    for slot in schedule:
        print('| {:^20} | {:>5} | {:>5} |'.format(slot.name, timestampToString(slot.startTime),
                                                  timestampToString(slot.endTime())))


if __name__ == "__main__":
    main()
