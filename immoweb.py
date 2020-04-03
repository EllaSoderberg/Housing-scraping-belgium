from selenium import webdriver

from bs4 import BeautifulSoup
import requests
import re
import json
import time
import calc_dist

def find_next(driver):
    try: 
        next_button = driver.find_element_by_xpath("//*[@class='pagination__link pagination__link--next button button--text']")
    except Exception:
        next_button = None
    return next_button

def get_links(link):
    """
    INPUT: link: The link of a manually performed search, webdriver: the path to the webdriver
    OUTPUT: apt_list: a list to all the apartments within the search
    """

    driver = webdriver.Chrome()  # Add path to chromedriver as an optional argument, if not specified it will search path.
    driver.get(link)
    
    apt_list = []
    
    while True:
        apts = driver.find_elements_by_xpath('//*[@class="card__title-link"]')

        time.sleep(5)

        for apt in apts:
            apt_list.append(apt.get_attribute("href"))

        next_button = find_next(driver)

        if next_button is None:
            break
        else:
            driver.get(next_button.get_attribute("href"))
        

    return apt_list


def get_info(link_list, loc_a, loc_b):
    """
    INPUT: link_list: A list of links to apartments, filename: the name of the file (.csv format), loc_a: a coordinate (format: "(long, lat)"), loc_b: a coordinate
    Saves the results as a .csv file
    """

    info_list = []

    for link in link_list:
        info_string = ""

        info_string += link
        info_string += ";"

        link_html = requests.get(link)
        soup = BeautifulSoup(link_html.content, 'html.parser')

        main_content = soup.find('div', class_="container-main-content")
        info = main_content.script.string

        info_span = re.search(' = ', info).span()[1]

        jready_info = info[info_span:-10]
        json_info = json.loads(jready_info)

        price_info = json_info["price"]
        price = price_info["mainValue"]
        extra_costs = price_info["additionalValue"]

        property_info = json_info["property"]
        bedrooms = property_info["bedroomCount"]
        has_garden = property_info["hasGarden"]
        has_balcony = property_info["hasBalcony"]
        has_basement = property_info["hasBasement"]
        has_attic = property_info["hasAttic"]
        # has_lift = property_info["hasLift"]
        has_sauna = property_info["hasSauna"]
        area = property_info["netHabitableSurface"]

        location_info = property_info["location"]
        # floor = location_info["floor"]
        latitude = location_info["latitude"] 
        longitude = location_info["longitude"]
        street = location_info["street"]
        number = location_info["number"]

        statistics = json_info["statistics"]
        bookmarks = statistics["bookmarkCount"]
        view_count = statistics["viewCount"]

        availability = json_info["transaction"]
        # available = availability["availabilityDate"]
        certificates = availability["certificates"]
        try:
            energy_consumption = certificates["primaryEnergyConsumptionPerSqm"]
        except Exception:
            energy_consumption = "None"

        address = str(street) + " " + str(number)
        info_string += address
        info_string += ";"
        info_string += str(area)
        info_string += ";"
        info_string += str(energy_consumption)
        info_string += ";"
        info_string += str(bedrooms)
        info_string += ";"
        info_string += str(price)
        info_string += ";"
        info_string += str(extra_costs)
        info_string += ";"
        
        avg_distance, center = calc_dist.calc_distance(latitude, longitude, loc_a, loc_b)
        info_string += str(avg_distance)
        info_string += ";"
        info_string += str(center)
        info_string += ";"

        info_string += str(has_garden)
        info_string += ";"
        info_string += str(has_balcony)
        info_string += ";;;"
        info_string += str(has_attic)
        info_string += ";"
        info_string += str(has_basement)
        info_string += ";"
        info_string += str(has_sauna)
        info_string += ";"
        info_string += str(bookmarks)
        info_string += ";"
        info_string += str(view_count)
        info_string += "\n"

        info_list.append(info_string)

    return info_list