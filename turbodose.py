import selenium
import time
import re
from notify_run import Notify
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# load configuration files for city and notify-run channels
import pathlib
file_path = pathlib.Path(__file__).parent.absolute()
with open(str(file_path)+"/city_config.txt","r") as f:
    city_and_address = json.load(f)

# iterate over city
for key in city_and_address.keys():
    city = key
    city_endpoint = city_and_address[key]
    
    # create notifier
    notify = Notify(endpoint="https://notify.run/"+city_endpoint)

    # Selenium configuration
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # Regex configuration
    hour_pattern = re.compile("\d{1,2}[:]\d{2}")

    # Logger configuration
    logging.basicConfig(filename=str(file_path)+'/turbolog.log',
                        format="%(asctime)s : %(levelname)s : %(message)s",
                        level=logging.INFO, datefmt="%a - %H:%M:%S-%d/%m/%Y")


    # Main Loop
    logging.info("Starting main loop for : "+city)
    # Get page
    driver.get("https://www.doctolib.fr/vaccination-covid-19/"+city)
    # Click refuse cookie button
    driver.find_element_by_id("didomi-notice-disagree-button").click()
    # Click 18 ans non prioritaire
    driver.find_element_by_id("eligibility-3").click()
    # Click "Rechercher"
    driver.find_element_by_xpath("/html/body/div[14]/div[2]/div/div[3]/button").click()

    logging.info("Scrolling")

    # Get height
    height = driver.execute_script("return document.body.scrollHeight")
    # Scroll to load all results
    for i in range(0,height-1000,500):
        driver.execute_script("window.scrollTo(0, {});".format(i))
        time.sleep(0.2) # slow down scrolling to allow results to load

    logging.info("Getting results")

    # Get results
    results = driver.find_elements_by_class_name("dl-search-result")

    logging.info("Processing results")

    # Process results
    #     
    for res in results :
        # Find hours, if any
        hits = re.findall(hour_pattern, res.text)

        if len(hits)>0:
            print("rdv!")
            logging.info("======= Rdv found !")
            # Get location doctolib page url
            place_url = res.find_element_by_class_name("dl-button-primary").get_attribute("href")

            list_content = res.text.split("\n")
            h_idx= list_content.index(hits[0])

            logging.info(" ".join(["💉 dispo ! 📅",
                                  list_content[h_idx-2],
                                  list_content[h_idx-1],
                                  "⏰",list_content[h_idx]]))

            logging.info(place_url)

            logging.info("sending notification")
            
            notify.send(" ".join(["💉 dispo ! 📅",
                                  list_content[h_idx-2],
                                  list_content[h_idx-1],
                                  "⏰",list_content[h_idx]]),
                       place_url)

    logging.info("Main loop over")
    driver.quit()
