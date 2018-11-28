from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import smtplib

class Flight:   #Flight Class used to store departure time, arrival time, and price data
    pass

def find_flights(start, end, date): #function to create list of flights leaving on a day
    driver = webdriver.Chrome("C:\\webdrivers\\chromedriver.exe")
    driver.get('https://www.southwest.com')

    oneway = driver.find_element_by_id('trip-type-one-way').click()

    origin = driver.find_element_by_id('air-city-departure')
    origin.send_keys(start)

    destination = driver.find_element_by_id('air-city-arrival')
    destination.send_keys(end)

    departure = driver.find_element_by_id('air-date-departure')
    for i in range(0,5):
        departure.send_keys(Keys.BACKSPACE)
    departure.send_keys(date)

    origin.submit()

    time.sleep(5)

    driver.find_element_by_xpath("//input[@aria-label='Sort results by']").click()

    driver.find_element_by_xpath("//span[contains(text(), 'Price')]/parent::*").click()

    times = driver.find_elements_by_class_name("time--value")
    price = driver.find_elements_by_class_name("fare-button--value-total")
    flight_class = []

    num = len(times)//2

    for f in range(num):
        xyz = Flight()
        xyz.name = (times[f*2].get_attribute("innerText") + ' to ' + end)
        xyz.departure = times[f*2].get_attribute("innerText")
        xyz.arrival = times[f*2+1].get_attribute("innerText")
        xyz.price = price[f*3+2].get_attribute("innerText")
        flight_class.append(xyz)

    driver.quit()

    return flight_class

def sendemail(subject, message,
              smtpserver='smtp.gmail.com:587'):

    header  = 'From: mcdevacct@gmail.com\n'
    header += 'To: mrussellclarke@gmail.com\n'
    # header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login('mcdevacct','S0uthw3stD3v')
    problems = server.sendmail('mcdevacct@gmail.com', 'mrussellclarke@gmail.com', message)
    server.quit()
    return problems
