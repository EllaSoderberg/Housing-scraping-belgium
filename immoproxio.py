from selenium import webdriver
import time

from bs4 import BeautifulSoup
import requests
import re
import json

import calc_dist


def get_links(link):
    """
    INPUT: link: The link of a manually performed search, webdriver: the path to the webdriver
    OUTPUT: apt_list: a list to all the apartments within the search
    """
    driver = webdriver.Chrome()  # Add path to chromedriver as an optional argument, if not specified it will search path.    driver.get(link)

    apt_list = []

    next_button = driver.find_element_by_id("paging_next")

    while(next_button != None):
        apts = driver.find_elements_by_class_name("img")
        time.sleep(3)
        for apt in apts:
            apt_list.append(apt.get_attribute("href"))
        driver.get(next_button.find_element_by_tag_name('a').get_attribute("href"))
        try:
            next_button = driver.find_element_by_id("paging_next")
        except Exception:
            next_button = None

    return apt_list

def get_info(link_list, loc_a, loc_b):
    """
    INPUT: link_list: A list of links to apartments, filename: the name of the file (.csv format), webdriver: the path to the webdriver, loc_a: a coordinate (format: "(long, lat)"), loc_b: a coordinate
    Saves the results as a .csv file
    """

    info_list = []

    for link in link_list:

        info_string = ""

        info_string += link
        info_string += ";"

        driver = webdriver.Chrome()  # Add path to chromedriver as an optional argument, if not specified it will search path.        
        driver.get(link)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        info = soup.find_all('script')
        for i in info:
            if i.string != None:
                search = re.search("getsetFitabisPanden()", i.string)
                if search != None: 
                    info = i.string


        info_span = re.search(' = ', info).span()[1]
        info_span_end = re.search('"CurrentLang":""', info).span()[1]

        jready_info = info[info_span:info_span_end] + '}]}'
        json_info = json.loads(jready_info)

        # available = json_info["Available"]
        price = json_info["Price"]
        extra_costs = json_info["MonthlyCost"]
        area = json_info["AreaGround"]

        address = json_info["Address"]
        street = address["Street"]
        number = address["Number"]
        latitude = address["Latitude"] 
        longitude = address["Longitude"]

        garden = json_info["DirectionGarden"]
        # floor = json_info["Floor"]
        bedrooms = json_info["MinBedrooms"]

        energy_consumption = json_info["ValueEPC"]

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

        info_string += str(garden)
        info_string += ";;;;;;;;\n"

        driver.close()

        info_list.append(info_string)

    return info_list
