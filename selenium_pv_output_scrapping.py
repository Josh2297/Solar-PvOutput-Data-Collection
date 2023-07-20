'''Date: July 1, 2023
By: Okechukwu Joshua Ifeanyi / 
Project: Anuka Stanley
PV output forecast scrapping script.
Site: Pvoutput.org '''


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import logging
import os
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(filename='pv_output_logs.txt', level=logging.DEBUG)


# Mini Function
def extract_date_generated_power(
    tag_object, 
    date_list: list, 
    generated_list:list , 
    station_name=None
) -> list:
    for generated in tag_object:
        # Find Generated Power
        try:
            date = generated.find('td').find('a').string
            gen = generated.find_all('td')[1].string
            date_list.append(date)
            generated_list.append(gen)
        except Exception:
            logging.debug(
                f'Date and generated Missing, Ladder: {station_name}'
            )
            pass


def page_scrape(driver, station_name):
        data_list = [[], []]
        print(f'Station: {station_name}')
        FLAG = True
        for _ in range(12):
            if FLAG == True:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located(
                        (By.LINK_TEXT, 'Target')
                    )
                )
                soup = bs(driver.page_source, 'html.parser')
                tag_object = soup.find_all("table")[1].find_all('tr')[2:]
                # Call Main Function
                main(tag_object, data_list, station_name)
                FLAG = False
            else:
                driver.implicitly_wait(10)
                try:
                    driver.find_element(By.LINK_TEXT, 'Next').click()
                except:
                    print('Page End')
                    break
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located(
                        (By.LINK_TEXT, 'Target')
                    )
                )
                soup = bs(driver.page_source, 'html.parser')
                tag_object = soup.find_all("table")[1].find_all('tr')[2:]
                # Call Main Function
                main(tag_object, data_list, station_name)
        data_list = {'Date': data_list[0], 'Generated Power': data_list[1]}
        try:
            pd_data = pd.DataFrame(data_list)
            print(pd_data.head(5))
            pd_data.to_csv(
                os.path.join(
                    dirname, 
                    'pv_output', 
                    f'{station_name}_data.csv'
                ), 
                index=False
            )
        except Exception as err:
            logging.debug(
                f'{station_name} Failed to save to CSV, Array Length error'
            )
            print(err)
            pass


# Mini Function
def main(
        tag_object, 
        data_list: list, 
        station_name
    ) -> None: 
    # Call the mini function
    gen = extract_date_generated_power(
        tag_object, 
        data_list[0], 
        data_list[1], 
        station_name
    )


def specific_ladder(driver, ladder):
        # Get the parent
        parent = ladder.find_element(
            By.XPATH, '..'
            ).find_element(
                By.XPATH, 
                '..'
            )
        station = parent.find_elements(
            By.XPATH, '*'
            )[2].find_element(
                By.TAG_NAME, 
                'a'
            )
        station_name = station.text
        station.click()
        page_scrape(driver, station_name)
        driver.implicitly_wait(10)


def get_healthy_ladders(driver):
    # Find percentage health
    health = driver.find_elements(By.TAG_NAME, 'small')
    list_of_health = [h for h in health if re.search(r'%|N/A', h.text)]
    healthy_ladders = []
    for num in list_of_health:
        if re.search(r'^(\d+)', num.text) and int(num.text[:-1]) >= 98:
            healthy_ladders.append(num)
    return healthy_ladders


def healthy_ladders(driver, ladder_page):
    num = len(get_healthy_ladders(driver))
    print(f'Num: {num}')
    for x in range(0, num):
        ladder = get_healthy_ladders(driver)[x]
        # call specific ladder
        specific_ladder(driver, ladder)
        # Take Back to ladder page
        driver.find_element(By.LINK_TEXT, 'PV Ladder').click()
        driver.implicitly_wait(5)
        driver.find_element(By.LINK_TEXT, str(ladder_page)).click()
        driver.implicitly_wait(5)

        print('I have ran')


if __name__ == "__main__":
    dirname = os.path.dirname(os.path.realpath(__file__))
    data_list = [[], []]
    url = "https://pvoutput.org/login.jsp"
    login_username = ''
    login_password = ''
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)
    driver.find_element('id', 'login').send_keys(login_username)
    driver.find_element('id', 'password').send_keys(login_password)
    driver.find_elements(By.TAG_NAME, 'input')[2].click()
    ####
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, 'PV Ladder').click()
    for x in range(1, 10):
        try:
            driver.find_element(By.LINK_TEXT, str(x+1)).click()
            driver.implicitly_wait(10)
        except:
            print('No Next Page')
        print(f'Ladder Page: {x+1}')
        ladders = driver.find_elements(By.TAG_NAME, 'a')
        list_of_ladders = [ladder for ladder in ladders if re.search(
                r'list.jsp\?id=',ladder.get_attribute(
                    'href'
                )
            )
        ]
        print(f'Length of Ladders: {len(list_of_ladders)}')
        healthy_ladders(driver, x+1)
        # Take Back to ladder page
        driver.find_element(By.LINK_TEXT, 'PV Ladder').click()
        driver.implicitly_wait(10)

    driver.quit()
