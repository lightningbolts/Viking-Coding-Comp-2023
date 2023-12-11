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
    minutesPerDay = stringToTimestamp("24:00")

    start = timestampInput("\tEarliest acceptable time: ")
    while start >= minutesPerDay:
        print("Please keep the time between 0:00 and 23:59")
        start = timestampInput("\tEarliest acceptable time: ")

    end = timestampInput("\tLatest acceptable time: ")
    while end >= minutesPerDay:
        print("Please keep the time between 0:00 and 23:59")
        end = timestampInput("\tLatest acceptable time: ")

    return tuple([start, end])


def letter(n):
    return chr(ord('A') + n)


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


class ClassPeriod(Slot):
    def __init__(self, periodNumber, startTime, length, lunchNum = None):
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
    passLen = intInput("How long is each passing period? (minutes) ")
    lunchLen = intInput("How long is lunch? (minutes) ")
    while True:
        firstLunchStartTimes = rangeInput("When does first lunch start? (24-hour time) ")
        if firstLunchStartTimes[0] < startTime or firstLunchStartTimes[-1] > latestEndTime:
            print("Please make sure lunch starts after school starts or before school ends. ")
        break
    numLunches = intInput("How many lunches are there? ")

    try:
        printSchedule(*scheduler(numPeriods, startTime, latestEndTime, passLen, lunchLen, firstLunchStartTimes, numLunches))
    except InvalidSchedule:
        print("Error: There is no valid schedule under the conditions you specified.")


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
    if passLen == 0:
        raise InvalidSchedule
    periodLen = math.floor(((maxDayLen - lunchAndPassLen) / numPeriods - passLen))
    periodAndPassLen = periodLen + passLen
    schedule = []

    if periodLen <= 0:
        raise InvalidSchedule

    '''
    First lunch start time calculations
    '''
    numPeriodsBeforeLunch = math.floor((firstLunchStartTimes[0] - startTime) / periodAndPassLen)
    firstLunchStartTime = startTime + (numPeriodsBeforeLunch * periodAndPassLen)
    if firstLunchStartTime < firstLunchStartTimes[0]:
        while firstLunchStartTime < firstLunchStartTimes[0]:
            numPeriodsBeforeLunch += 1
            firstLunchStartTime += periodAndPassLen
        if firstLunchStartTime > firstLunchStartTimes[1]:
            raise InvalidSchedule

    if firstLunchStartTime < firstLunchStartTimes[0]:
        raise InvalidSchedule

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
        addClass(i, startTime + lunchAndPassLen + i*periodAndPassLen, periodLen)

    schedule.sort(key=lambda slot: slot.startTime)

    # Sort the schedule by start time
    return (periodLen, schedule)


def printSchedule(periodLen, schedule):
    print()
    print("Schedule")
    print("="*20)
    print(f"Classes are {periodLen} minutes long")
    print('| {:^20} | {:^5} | {:^5} |'.format("NAME", "START", "END"))
    for slot in schedule:
        print('| {:^20} | {:>5} | {:>5} |'.format(slot.name, timestampToString(slot.startTime), timestampToString(slot.endTime())))


if __name__ == "__main__":
    main()
