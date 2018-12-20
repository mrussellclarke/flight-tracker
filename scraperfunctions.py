from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import smtplib, imaplib, time, datetime, email, re

class Flight:   #Flight Class used to store departure time, arrival time, and price data
    pass

def find_flights(start, end, date): #function to create list of flight class objects leaving on a day
    driver = webdriver.Chrome("C:\\webdrivers\\chromedriver.exe")

    try:
        driver.get('https://www.southwest.com')

        driver.find_element_by_id('trip-type-one-way').click()

        origin = driver.find_element_by_id('air-city-departure')
        origin.send_keys(start)

        destination = driver.find_element_by_id('air-city-arrival')
        destination.send_keys(end)

        departure = driver.find_element_by_id('air-date-departure')
        for i in range(0,5):
            departure.send_keys(Keys.BACKSPACE)
        departure.send_keys(date)

        origin.submit()

        time.sleep(6)

        driver.find_element_by_xpath("//input[@aria-label='Sort results by']").click()

        driver.find_element_by_xpath("//span[contains(text(), 'Price')]/parent::*").click()

        times = driver.find_elements_by_class_name("time--value")
        price = driver.find_elements_by_class_name("fare-button--value-total")
        flight_class = []

        num = len(price)//3
        print('price size: ' +str(len(price)))
        print('times size: ' +str(len(times)))

        for f in range(num):
            xyz = Flight()
            xyz.name = (times[f*2].get_attribute("innerText") + ' to ' + end)
            xyz.departure = times[f*2].get_attribute("innerText")
            xyz.arrival = times[f*2+1].get_attribute("innerText")
            xyz.price = price[f*3+2].get_attribute("innerText")
            flight_class.append(xyz)

        print('complete')

    except:
        print('Some error message')

    driver.quit()

    return flight_class


def sendemail(subject, message, smtpserver='smtp.gmail.com:587'):
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

def check_mail():
    email = readmail()
    keywords = {}
    email_body = []

    # if 'mrussellclarke' in email['ef'] and 'flight' in email['es'].lower():
    if 'mcdevacct' in email['ef']:
        for line in email['eb'].splitlines():
            email_body += line.split(' ')

    for word in email_body:
        if re.match(r'(\d|\d\d)/(\d\d|\d)', word, re.I):
            if 'outdate' not in keywords:
                keywords['outdate'] = word
            else:
                keywords['indate'] = word
        elif len(word) == 3:
            # re.match(r'[A-z]{3}', word, re.I):
            if 'departure' not in keywords:
                keywords['departure'] = word
            else:
                keywords['arrival'] = word

    return keywords

def readmail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('mcdevacct@gmail.com', 'S0uthw3stD3v')

    mail.list()
    mail.select('inbox')

    result, data = mail.uid('search', None, "ALL")

    latest_email_uid = data[0].split()[-1]
    result, data= mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')

    email_message = email.message_from_string(raw_email_string)

    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            email_from = email_message['from']
            email_subject =  email_message['subject']
            email_body = body.decode('utf-8')

    return {'ef': email_from, 'es': email_subject, 'eb': email_body}

def new_mail(x, oldCheck): #check inbox for new flight email
    if x > 0:
        newCheck = check_mail()

        if (newCheck['departure'] == oldCheck['departure']
        and newCheck['arrival'] == oldCheck['arrival']
        and newCheck['outdate'] == oldCheck['outdate']):
            print('No new mail')
            time.sleep(5)
            new_mail(1, oldCheck)
        else:
            print('New mail!')

def new_price(fday): #checks to see if date of flight has happened
    cday = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day)

    if fday != cday:
        time.sleep(86400)
        new_price(fday)
    else:
        return
