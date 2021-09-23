import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# read inputs
# print("--- USC NetID Credentials ---");
# _USC_USER = input("User Name: ");
# _USC_PASS = input("Password: ");

_USC_USER = "terr"
_USC_PASS = "13jan199913jan1999"
_BOOKING_MONTH = "9"
_BOOKING_DAY = "24"


# open browser window
_GYM_URL = "https://myrecsports.usc.edu/booking"
browser = webdriver.Chrome()
browser.get(_GYM_URL)
browser.maximize_window()
browser.execute_script(
    "{showLogin('/booking');submitExternalLoginForm('Shibboleth');}")

# create action obj
action = ActionChains(browser)

with open('schedule.json', 'w+') as savedSched:
        if not savedSched.empty:
            print("You currently have a schedule saved, would you like to overwrite it?");
            input("y/n: ")
            
        sched = savedSched;
        json.dump(, f)


def runScheduler():

    try:
        # wait for usc shibboleth button to show up
        shibbolethBtn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='divLoginOptions']/div[2]/div[2]/div/button")))
        shibbolethBtn.click()

        # find user and pass input and login
        userInput = browser.find_element_by_id("username")
        passInput = browser.find_element_by_id("password")

        userInput.send_keys(_USC_USER)
        passInput.send_keys(_USC_PASS, Keys.ENTER)

        print(f"{_USC_USER} successfully logged in thru Shibboleth")

        # wait for usc login and then fitness button
        villageBookingsBtn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-product-id='cd93ade2-af9d-4e5f-84e0-06e10711b5ce']")))
        villageBookingsBtn.click()

        # find bbooking day button and select correct day
        bookingDayBtn = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='divBookingDateSelector']/div[2]//button[@data-day='{_BOOKING_DAY}']")))
        bookingDayBtn.click()

        # Find bookable times and locate book buttons
        bookingButtons = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[@data-timeslot-id]")))

        # Loop over buttons and check if times are compatible with chosen times
        for button in bookingButtons:
            bookingTime = button.get_attribute("data-slot-text")
            print(f"Opening found from {bookingTime}, checking compatibility...")

    except Exception as e:
        print(e)
    finally:
        browser.close()


