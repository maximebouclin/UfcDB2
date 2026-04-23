import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from string import ascii_lowercase as alc

# Program scrapes UFC website and retrieves information about all its fighters which it records in the fighter_info.cs
# output file to be used to load data into MySQL database
# AUTHOR - Maxime Bouclin

#SETUP
service = Service(ChromeDriverManager().install())  # Automatically gets the correct driver
driver = webdriver.Chrome(service=service)

#START OF GET FIGHTER INFO FUNCTION
def get_fighter_info():
    #Get fighter ID
    current_url = driver.current_url
    fighter_id = current_url.split("/")[-1] #id is the last part of the url
    print(fighter_id)

    #Get the fighter's name
    fighter_name = driver.find_element(By.CLASS_NAME, "b-content__title-highlight").text
    print(fighter_name)

    #Get nickname if exists
    try:
        fighter_nickname = driver.find_element(By.CLASS_NAME, "b-content__Nickname").text.strip()
        if not fighter_nickname:
            raise NoSuchElementException("Nickname value not available for this fighter")
    except (NoSuchElementException, IndexError) as e:
        fighter_nickname = "\\N"
    print(fighter_nickname)

    #Get stats
    fighter_stats = driver.find_elements(By.CLASS_NAME, "b-list__box-list-item_type_block")

    # Get height
    try:
        fighter_height_string = fighter_stats[0].text.strip("\"").strip("HEIGHT: ")
        if fighter_height_string == "--":
            raise NoSuchElementException("Height value not available for this fighter")
        else:
            fighter_feet_and_inches = fighter_height_string.split("\'")
            fighter_height_feet = int(fighter_feet_and_inches[0])
            fighter_height_inches = int(fighter_feet_and_inches[1])
            fighter_height = (12 * fighter_height_feet) + fighter_height_inches
    except (NoSuchElementException, IndexError) as e:
        fighter_height = "\\N"
    print(fighter_height)

    #Get weight
    try:
        fighter_weight = fighter_stats[1].text.strip(" lbs.").strip("WEIGHT: ")
        if fighter_weight == "--":
            raise NoSuchElementException("Weight value not available for this fighter")
    except (NoSuchElementException, IndexError) as e:
        fighter_weight = "\\N"
    print(fighter_weight)

    #Get reach
    try:
        fighter_reach = fighter_stats[2].text.strip("\"").strip("REACH: ")
        if fighter_reach == "--":
            raise NoSuchElementException("Reach value not available for this fighter")
    except (NoSuchElementException, IndexError) as e:
        fighter_reach = "\\N"
    print(fighter_reach)
    
    #Get stance
    try:
        fighter_stance = fighter_stats[3].text.strip("STANCE:").strip()
        if not fighter_stance:
            raise NoSuchElementException("Stance value not available for this fighter")
    except (NoSuchElementException, IndexError) as e:
        fighter_stance = "\\N"
    print(fighter_stance)
    
    #Get dob
    try:
        fighter_dob_string = fighter_stats[4].text.strip("DOB: ")
        if fighter_dob_string == "--":
            raise NoSuchElementException("Weight value not available for this fighter")

        # Remove the commas and periods
        fighter_dob_string = fighter_dob_string.replace(",", "")
        fighter_dob_string = fighter_dob_string.replace(".", "")

        # Divide the date into its core pieces
        fighterDobYear = fighter_dob_string.split(" ")[2]
        fighterDobMonth = fighter_dob_string.split(" ")[0]
        fighterDobDay = fighter_dob_string.split(" ")[1]

        # Rewrite the month into a number
        match fighterDobMonth:
            case "Jan":
                fighterDobMonth = "01"
            case "Feb":
                fighterDobMonth = "02"
            case "Mar":
                fighterDobMonth = "03"
            case "Apr":
                fighterDobMonth = "04"
            case "May":
                fighterDobMonth = "05"
            case "Jun":
                fighterDobMonth = "06"
            case "Jul":
                fighterDobMonth = "07"
            case "Aug":
                fighterDobMonth = "08"
            case "Sep":
                fighterDobMonth = "09"
            case "Oct":
                fighterDobMonth = "10"
            case "Nov":
                fighterDobMonth = "11"
            case "Dec":
                fighterDobMonth = "12"
            case _:
                raise NoSuchElementException("Debut month not in expected format")

        fighter_dob = fighterDobYear + "-" + fighterDobMonth + "-" + fighterDobDay
    except (NoSuchElementException, IndexError) as e:
        fighter_dob = "\\N"
    print(fighter_dob)


    #Return list of fighter info
    return [fighter_id, fighter_name, fighter_nickname, fighter_height, fighter_weight, fighter_reach, fighter_stance, fighter_dob]
#END OF GET FIGHTER INFO FUNCTION

#START OF CODE TO BE EXECUTED ON RUN
#Get the info of each fighter and write it to a csv file
with open('fighter_info.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Name", "Nickname", "Height", "Weight", "Reach", "Stance", "DOB"])
    #Get all the fighter links
    from string import ascii_lowercase as alc
    #For each character in the alphabet
    for i in alc:

        #Get the page of all fighters whose names start with that letter
        driver.get(f"http://ufcstats.com/statistics/fighters?char={i}&page=all")
        #Reset list of fighter links
        fighter_page_links = []
        #Wait until fighter links appear
        WebDriverWait(driver, 15).until(
                 EC.presence_of_element_located((By.CSS_SELECTOR, '.b-statistics__table-row > .b-statistics__table-col:first-child > a'))
             )
        #Get all fighter links
        fighterLinks = driver.find_elements(By.CSS_SELECTOR, '.b-statistics__table-row > .b-statistics__table-col:first-child > a')
        #For every link
        for link in fighterLinks:
            #Add url to list of fighter page links
            url = link.get_attribute("href")
            fighter_page_links.append(url)
        #For each url
        for j in fighter_page_links:
            driver.get(j) #Go to the url
            writer.writerow(get_fighter_info()) #Get the fighter's info and write it to the csv file
            time.sleep(0.1) # Wait 0.5s between fighters

#Close page
driver.quit()