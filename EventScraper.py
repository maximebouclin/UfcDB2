import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Program scrapes UFC website and retrieves information about all its events and fights
# which are then  event_info.cs
# output file to be used to load data into MySQL database
# AUTHOR - Maxime Bouclin - B00961893

def get_fight_urls_from_event(event_url):
    driver.get(event_url)
   
    # Create list of fight links
    fight_url_list = []

    # Wait until fight links appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.b-fight-details__table-body > tr'))
    )
    # Get all fight links for that event
    fightLinks = driver.find_elements(By.CSS_SELECTOR, '.b-fight-details__table-body > tr')

    # For every fight link
    for link in fightLinks:
        # Add url to list of event page links
        url = link.get_attribute("data-link")
        fight_url_list.append(url)

    return fight_url_list

def get_fight_info(fight_url, event_id):
    driver.get(fight_url)
    
    # Get fight ID
    current_url = driver.current_url
    fight_ID = current_url.split("/")[-1]  # id is the last part of the url
    print(fight_ID)

    #Get fighter ID's
    fighter_elements = driver.find_elements(By.CLASS_NAME, "b-fight-details__person-link")
    fighterIDs = list(map(get_fighter_id, fighter_elements))
    red_fighter_ID = fighterIDs[0]
    blue_fighter_ID = fighterIDs[1]
    print(red_fighter_ID)
    print(blue_fighter_ID)


    #FOR NEXT TIME, KEEP GETTING THE OTHER FIGHT STATS FROM HERE

    return [fight_ID, event_id, red_fighter_ID, blue_fighter_ID]

def get_fighter_id (fighter_element):
    return fighter_element.get_attribute("href").split("/")[-1]

def get_event_id(event_url):
    driver.get(event_url)

    # Get event ID
    current_url = driver.current_url
    event_id = current_url.split("/")[-1]  # id is the last part of the url
    return event_id

#START OF GET EVENT INFO FUNCTION
def get_event_info(event_url):
    driver.get(event_url)

    # Get event ID
    event_id = get_event_id(event_url)
    print(event_id)

    #Get event name
    event_name = driver.find_element(By.CLASS_NAME, "b-content__title-highlight").text
    print(event_name)

    #Get event details box
    event_details = driver.find_elements(By.CLASS_NAME, "b-list__box-list-item")

    #Get event location
    event_location = event_details[1].text.strip("LOCATION:").strip()
    print(event_location)
    
    #Get event date
    event_date_string = event_details[0].text.strip("DATE:").strip()
    
    # Remove the commas and periods
    event_date_string = event_date_string.replace(",", "")

    # Divide the date into its core pieces
    eventDobYear = event_date_string.split(" ")[2]
    eventDobMonth = event_date_string.split(" ")[0]
    eventDobDay = event_date_string.split(" ")[1]
    
    # Rewrite the month into a number
    match eventDobMonth:
        case "January":
            eventDobMonth = "01"
        case "February":
            eventDobMonth = "02"
        case "March":
            eventDobMonth = "03"
        case "April":
            eventDobMonth = "04"
        case "May":
            eventDobMonth = "05"
        case "June":
            eventDobMonth = "06"
        case "July":
            eventDobMonth = "07"
        case "August":
            eventDobMonth = "08"
        case "September":
            eventDobMonth = "09"
        case "October":
            eventDobMonth = "10"
        case "November":
            eventDobMonth = "11"
        case "December":
            eventDobMonth = "12"
        case _:
            raise NoSuchElementException("Debut month not in expected format")

    event_date = eventDobYear + "-" + eventDobMonth + "-" + eventDobDay
    
    print(event_date)
    
    return [event_id, event_name, event_location, event_date]
# END OF GET EVENT INFO FUNCTION


#START OF CODE TO BE EXECUTED ON EXECUTION
#Setup
service = Service(ChromeDriverManager().install())  # Automatically gets the correct driver
driver = webdriver.Chrome(service=service)

#Get the info of each event and write it to a csv file
with open('event_info.csv', 'w') as event_file, open('fight_info.csv', 'w') as fight_file:
    event_writer = csv.writer(event_file)
    event_writer.writerow(["ID", "Name", "Location", "Date"])
    fight_writer = csv.writer(fight_file)
    fight_writer.writerow(["ID", "event_ID", "red_fighter_ID", "blue_fighter_ID", "fight_weight_class_ID", 
                            "winner_ID", "outcome_method", "round_ended", "is_championship_fight", "red_sig_strikes_landed", 
                            "red_sig_strikes_attempted", "red_takedowns_landed", "red_takedowns_attempted", "red_sub_attempts", 
                            "red_control_secs", "blue_sig_strikes_landed", "blue_sig_strikes_attempted", "blue_takedowns_landed", 
                            "blue_takedowns_attempted", "blue_sub_attempts", "blue_control_secs", "referee_name"])
    
    #Get the page of all events
    driver.get("http://www.ufcstats.com/statistics/events/completed?page=all")
    
    #Create list of event links
    event_links = []
    
    #Wait until event links appear
    WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, '.b-statistics__table-row > .b-statistics__table-col:first-child > i > a'))
         )

    #Get all event links
    eventLinks = driver.find_elements(By.CSS_SELECTOR, '.b-statistics__table-row > .b-statistics__table-col:first-child > i > a')
    
    #For every link
    for link in eventLinks:
        #Add url to list of event page links
        url = link.get_attribute("href")
        event_links.append(url)

    #For each url
    for j in event_links:
        event_writer.writerow(get_event_info(j)) #Get the event's info and write it to the csv file
        fight_urls = get_fight_urls_from_event(j)
        event_id = get_event_id(j)
        for fight_url in fight_urls:
            fight_writer.writerow(get_fight_info(fight_url, event_id)) #Get the fight's info and write it to the csv file
        time.sleep(0.5) # Wait 0.5s between events

driver.quit() #Close page