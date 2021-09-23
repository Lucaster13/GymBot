import json
from icalendar import Calendar
import fileinput


_DOW = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]


def checkSched(sched): 
    while True:

        print("To choose a day, enter its number/letter")
        for idx, d in enumerate(_DOW):
            print(f"[{idx}]: {d}")
        print("[q]: QUIT")
        exit = False
        
        while True:
            dayIdx = input("\n:")
    
            if dayIdx == "q":
                exit = True
                break

            try:
                dayIdx = int(dayIdx)
                if dayIdx >= 0 and day < 7:
                    showDay(sched, dayIdx)
                    if not input("Enter 'y' to edit new day OR any other key to quit: ") == "y":
                        break
                else:
                    raise Exception()
            except Exception:
                print(f"Invalid choice: '{dayIdx}', please try again")

        if exit:
            break

def showDay(sched, dayIdx): 
    day = sched[dayIdx]

    print(f"--- {day.name} ---\n")
    print(json.dumps(day, indent=2))

    print("What would you like to do:")
    print("[1]: add new availability")
    print("[2]: delete availability")
    if day.activeBooking is not None:
        print("[3]: cancel active booking")
    print("[q]: QUIT")

    while True:
        num = input("\n:")
    
        if num == "q":
            break

        try:
            num = int(num)
            if num >= 1 and num < 4:
                {
                    1: addNewAvail,
                    2: deleteAvail,
                    3: cancelActiveBooking
                }[num](sched, dayIdx)
            else:
                raise Exception()
        except Exception:
            print(f"Invalid choice: '{num}', please try again")

def addNewAvail(sched, dayIdx):
    currAvails = sched[dayIdx].availabilities
    print(f"Current Availabilities: {currAvails}")
    print("Add New Availability:")
    print("Times must be in the form hh:mm am/pm\n")
    startTimeFull = input("Start Time: ");
    endTimeFull = input("End Time: ");
    overlaps = checkIsValidAvail(startTimeFull, endTimeFull, currAvails);

    if overlaps == 0:
        # add directly
        sched[dayIdx].availabilites.push(f"{startTimeFull} - {endTimeFull}")
    if overlaps.len > 0:
        if input(f"Would you like to merge {overlaps} with {newAvail}"):
            


def checkIsValidAvail(newAvail, currAvails):
    


def mergeAvails()
    
def deleteAvail(sched, dayIdx):

def cancelActiveBooking(sched, dayIdx):            

def cleanSchedule(sched):


def makeSched():
    # open json file to check data


    icsFile = open(fileinput.input(input()), 'rb');
    userSchedule = Calendar.from_ical(icsFile.read());

    schedule = 

    input()
    
