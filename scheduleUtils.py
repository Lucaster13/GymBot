import json
import traceback
from time import daylight

_SAVED_SCHEDULE_FILE = 'schedule.json'
_DOW = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]




def modifySched(): 
    while True:

        sched = getSavedScheduleFromFile()

        print("To choose a day, enter the value in the brackets.\n")
        for idx, d in enumerate(_DOW):
            print(f"[{idx}]: {d}")
        if not sched["empty"]:
            print("[clear]: CLEAR SCHEDULE")
        print("[q]: QUIT")
        
        exit = False
        
        while True:
            option = input("\n: ")
            try:
                if option == "q":
                    exit = True
                    break
                elif option == "clear":
                    if input("Are you sure you want to clear your schedule? [y/n]: ") == "y":
                        clearSched()
                        createSched()
                else:
                    option = int(option)
                    if option >= 0 and option < 7:
                        modifyDay(_DOW[option])
                        print("[y]: edit different day")
                        print("[q]: quit")
                        if not input("\n: ") == "y":
                            break
                    else:
                        print(f"\nInvalid choice: '{option}', please try again")
            except Exception as e:
                print("\n\n", traceback.print_exc(), "\n\n")
                    
        if exit:
            break

def modifyDay(dow):
    sched = getSavedScheduleFromFile()
    day = sched[dow]
    isEmptyDay = len(day["availabilities"]) > 0

    print(f"\n--- {day['name']} ---")
    printDay(day)

    print("What would you like to do:")
    print("[1]: add new availability")
    if isEmptyDay:
        print("[2]: delete availability")
        print("[3]: modify existing availability")
        print("[4]: clear availabilities")
    if day["activeBooking"] is not None:
        print("[6]: cancel active booking")
    print("[q]: QUIT")

    while True:
        num = input("\n: ")
    
        if num == "q":
            break

        num = int(num)
        if num >= 1 and num < 4:
            {
                1: addNewAvail,
                2: deleteAvail,
                4: modifyAvail,
                5: clearAvails,
                # 6: cancelActiveBooking
            }[num](dow)
        else:
            print(f"\nInvalid choice: '{num}', please try again")

def addNewAvail(dow):
    sched = getSavedScheduleFromFile()
    currAvails = sched[dow]["availabilities"]

    while True: 
        print("\n--- Current Availabilities ---")
        printAvails(currAvails)
        print("\n--- Add New Availability (Time Format hh:mm am/pm) ---\n")

        startTimeFull = input("Start Time: ").strip();
        endTimeFull = input("End Time: ").strip();
        newAvailStr = f"{startTimeFull} - {endTimeFull}";
        newValidAvail = checkIsValidAvail(newAvailStr)

        if newValidAvail is not None:
            print(f"\nAttempting to add new availability ({newValidAvail['fullTime']})...")
            # check for overlaps
            overlaps = findOverlaps(newValidAvail, currAvails)
            if len(overlaps) == 0:
                # add directly
                sched[dow]['availabilities'].append(newValidAvail)
            else:
                print(f"New availability {newValidAvail} overlaps with {overlaps}");
                if input("Would you like to merge these? [y/n]: ") == "y":
                    mergeAvails(newValidAvail, overlaps, dow)
            
            # overwrite saved sched
            print(f"Successfully added new availability {newValidAvail['fullTime']}!")
            saveScheduleToFile(sched)
            print(f"Availabilities for {sched[dow]['name']}:")
            printAvails(sched[dow]["availabilities"])

        if input("\nEnter q to quit, or any other key to add another availability: ") == "q":
                break

def deleteAvail(dow):
    sched = getSavedScheduleFromFile()
    currAvails = sched[dow]["availabilities"]
    print("Which availability would you like to delete:")

    while True:
        
        for idx, avail in enumerate(currAvails):
            print(f"[{idx}]: {avail['fullTime']}")
        print("[q]: QUIT")

        num = input("\n:")
    
        if num == "q":
            break

        num = int(num)
        if num >= 0 and num < len(currAvails):
            print(f"Attempting to delete availability ({currAvails[num]['fullTime']})...")
            del sched[dow]["availabilities"][num]
            saveScheduleToFile(sched)
            print("[y]: delete another availability")
            print("[q]: quit")
            if not input("\n: ") == "y":
                break
        else:
            print(f"\nInvalid choice: '{num}', please try again.")

        

def modifyAvail(dow):
    sched = getSavedScheduleFromFile()
    currAvails = sched[dow]["availabilities"]
    print("Which availability would you like to modify:")

    while True:

        for idx, avail in enumerate(currAvails):
            print(f"[{idx}]: {avail['fullTime']}")
        print("[q]: QUIT")

        num = input("\n: ")
    
        if num == "q":
            break

        num = int(num)
        if num >= 0 and num < len(currAvails):
            currAvail = currAvails[num]
            print("Times must be in the form hh:mm am/pm\n")

            startTimeFull = input(f"Start Time (currently {currAvail['fullTime'].split('-')[0].strip()}): ");
            endTimeFull = input(f"End Time (currently {currAvail['fullTime'].split('-')[1].strip()}): ");

            newAvailStr = f"{startTimeFull} - {endTimeFull}";

            print(f"Attempting to change availability ({currAvails[num]['fullTime']}) to ({newAvailStr})...")

            newValidAvail = checkIsValidAvail(newAvailStr)

            if newValidAvail is not None:
                overlaps = findOverlaps(newValidAvail, currAvails)
                
                # always one overlap, if more, prompt user
                if len(overlaps) > 1:
                    print(f"Modified availability {newValidAvail} now overlaps with {overlaps}");
                    if input("Would you like to merge these? [y/n]: "):
                        mergeAvails(newValidAvail, overlaps, dow)
                else:
                    mergeAvails(newValidAvail, overlaps, dow)

            saveScheduleToFile(sched)
            print("[y]: modify different availability")
            print("[q]: quit")
            if not input("\n: ") == "y":
                break
        else:
            print(f"\nInvalid choice: '{num}', please try again.")
        

def clearAvails(dow):
    sched = getSavedScheduleFromFile()
    if input(f"Are you sure you want to clear availabilities for {sched[dow]['name']}? [y/n]: ")  == "y":
        print(f"Clearing availabilities for {sched[dow]['name']}")
        sched[dow]["availabilities"] = []
        saveScheduleToFile(sched)

# def cancelActiveBooking(sched, dayIdx):    

def checkIsValidAvail(newAvailStr):
    availObj = makeAvailObjFromStr(newAvailStr)

    sHrs = availObj["startTime"]["hrs"]
    sMins = availObj["startTime"]["mins"]
    eHrs = availObj["endTime"]["hrs"]
    eMins = availObj["endTime"]["mins"]

    sArmy = availObj["startTime"]["army"]
    eArmy = availObj["endTime"]["army"]

    isValidHrs = sHrs >= 0 or sHrs <= 12 or eHrs >= 0 or eHrs <= 12
    isValidMins = sMins >= 0 or sMins <= 59 or eMins >= 0 or eMins <= 59
    isValidTime = eArmy >= sArmy

    if not isValidHrs or not isValidMins or not isValidTime:
        print(f"\nInvalid availability provided: {newAvailStr}, please check syntax and try again")     
        return None
    else:
        return availObj
        
        

def makeAvailObjFromStr(availStr):
    # availStr takes the following form: hh:mm am/pm - hh:mm am/pm 

    fullTimes = availStr.split("-")
    startTime = fullTimes[0].strip();
    endTime = fullTimes[1].strip();

    startTimeObj = getTimeComponents(startTime)
    endTimeObj = getTimeComponents(endTime)

    sHrsFormat = startTimeObj["hrs"] if startTimeObj["hrs"] >= 10 else f"0{startTimeObj['hrs']}"
    sMinsFormat = startTimeObj["mins"] if startTimeObj["mins"] >= 10 else f"0{startTimeObj['mins']}"
    sAmPm = startTimeObj["amPm"]
    eHrsFormat = endTimeObj["hrs"] if endTimeObj["hrs"] >= 10 else f"0{endTimeObj['hrs']}"
    eMinsFormat = endTimeObj["mins"] if endTimeObj["mins"] >= 10 else f"0{endTimeObj['mins']}"
    eAmPm = endTimeObj["amPm"]

    fullTime = f"{sHrsFormat}:{sMinsFormat} {sAmPm} - {eHrsFormat}:{eMinsFormat} {eAmPm}"

    return {
        "fullTime": fullTime,
        "startTime": startTimeObj,
        "endTime": endTimeObj
    }

def getTimeComponents(timeStr):
    # timeStr takes form ---> hh:mm am/pm
    timeComponents = timeStr.split(" ");
    time = timeComponents[0].strip().split(":")
    amPm = timeComponents[1].strip()
    hrs = int(time[0].strip())
    mins = int(time[1].strip())
    armyTime = getArmyTime(hrs, mins, amPm)
        
    return {
        "amPm": amPm,
        "hrs": hrs,
        "mins": mins,
        "army": armyTime
    }

def getArmyTime(hrs, mins, amPm):
    minsFormatted = mins if mins > 10 else f"0{mins}"
    hrsFormatted = ""
    if amPm == "pm":
        if hrs == 12:
            hrsFormatted = hrs
        else:
            hrsFormatted = hrs + 12
    elif amPm == "am":
        if hrs == 12:
            hrsFormatted = "00"
        else:
            hrsFormatted = hrs
    else:
        # invalid amPm
        raise Exception()

    return f"{hrsFormatted}:{minsFormatted}"

def findOverlaps(newAvail, currAvails):
    # filter all availabilities that overlap newAvail
    return list(filter(lambda avail: isOverlap(newAvail, avail), currAvails))

def isOverlap(avail1, avail2):
    sArmy1 = avail1["startTime"]["army"]
    sArmy2 = avail2["startTime"]["army"]

    eArmy1 = avail1["endTime"]["army"]
    eArmy2 = avail2["endTime"]["army"]

    if sArmy1 < sArmy2:
        return eArmy1 >= sArmy2
    elif sArmy1 == sArmy2:
        return True
    else:
        return sArmy1 <= eArmy2
        
def mergeAvails(newAvail, overlaps, dow):
    sched = getSavedScheduleFromFile()

    # get smallest start time and largest end time
    # overlaps are sorted, compare newAvail w first and last overlap
    startTime = {}
    endTime = {}
    currStartTime = overlaps[0]["startTime"]["army"]
    currEndTime = overlaps[len(overlaps) - 1]["endTime"]["army"]

    if newAvail["startTime"]["army"] < currStartTime:
        startTime = newAvail["startTime"]
    else:
        startTime = overlaps[0]["startTime"]

    if newAvail["endTime"]["army"] > currEndTime:
        endTime = newAvail["endTime"]
    else:
        endTime = overlaps[len(overlaps) - 1]["endTime"]

    mergedAvail = {
        "fullTime": f"{startTime['hrs']}:{startTime['mins']} {startTime['amPm']} - {endTime['hrs']}:{endTime['mins']} {endTime['amPm']}",
        "startTime": startTime,
        "endTime": endTime
    }

    # remove overlaps from sched and add new merged avail
    avails = sched[dow]["availabilities"]
    modifiedAvails = list(filter(lambda avail: not isOverlap(avail, mergedAvail), avails))
    modifiedAvails.append(mergedAvail)

    # set schedule
    sched[dow]["availabilities"] = modifiedAvails

def saveScheduleToFile(sched):
    
    # check if empty
    isEmpty = True
    for attr, dayObj in sched.items():
        if not attr == "empty" and len(dayObj["availabilities"]) > 0:
            isEmpty = False
            break
    sched["empty"] = isEmpty

    # sort all availabilities by start times
    for attr, obj in sched.items():
        if not attr == "empty":
            sched[attr]["availabilities"].sort(key=lambda avail: avail["startTime"]["army"])

    with open(_SAVED_SCHEDULE_FILE, 'w') as schedFile:
        print(f"Saving schedule to {_SAVED_SCHEDULE_FILE}")
        json.dump(sched, schedFile)
    

def getSavedScheduleFromFile():
    with open(_SAVED_SCHEDULE_FILE, 'r') as schedFile:
        return json.load(schedFile)
    
def clearSched():
    # write empty schedule to file
    saveScheduleToFile({
        "empty": True
    })

def createSched():
    sched = {
        "empty": True
    }
    for dow in _DOW:
        sched[dow] = {
            "name": dow + "day",
            "availabilities": [],
            "activeBooking": None,
        }
    with open(_SAVED_SCHEDULE_FILE, 'w') as schedFile:
        json.dump(sched, schedFile)
    modifySched()

def isCompatible(bookingTimeStr, dow):
    day = getSavedScheduleFromFile()[dow]
    spansNoon = "am" in bookingTimeStr.split("-")[0].strip()

    bookingTimeObj = {}

    # create the booking time obj
    if spansNoon:
        # bookingTime is valid format
        bookingTimeObj = makeAvailObjFromStr(bookingTimeStr)
    else:
        # fix format of bookingTime
        amPm = bookingTimeStr.split("-")[1].strip().split(" ")[1].strip()
        bookingStart = f"{bookingTimeStr.split('-')[0].strip()} {amPm}"
        bookingEnd = bookingTimeStr.split("-")[1].strip()
        validBookingTimeStr = f"{bookingStart} - {bookingEnd}"
        bookingTimeObj = makeAvailObjFromStr(validBookingTimeStr)

    # find overlaps for bookingTime
    overlaps = findOverlaps(bookingTimeObj, day["availabilities"])

    for overlap in overlaps:
        bookingStart = bookingTimeObj["startTime"]["army"]
        availStart = overlap["startTime"]["army"]

        bookingEnd = bookingTimeObj["endTime"]["army"]
        availEnd = overlap["endTime"]["army"]

        # compatible booking found if this evaluates to true
        return bookingStart >= availStart and bookingEnd <= availEnd
      
    return False

def createActiveBooking(bookingTime, dow):
    sched = getSavedScheduleFromFile()
    print(f"Creating new active booking in schedule for {sched[dow]['name']} at {bookingTime}")
    sched[dow].activeBooking = bookingTime
    saveScheduleToFile(sched)

def printAvails(avails):
    print(json.dumps(list(map(lambda a: a["fullTime"], avails)), indent=2))

def printDay(day):
    avails = day['availabilities']
    day['availabilities'] = list(map(lambda a: a["fullTime"], avails))
    print(json.dumps(day, indent=2), "\n")