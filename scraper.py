from scraperfunctions import find_flights, check_mail, sendemail
import threading, time, datetime
# import multiprocessing

def flight_day(fday): #checks to see if date of flight has happened
    cday = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day)

    if fday == cday:
        return 1
    else:
        return 0

flight_req = check_mail()

lday = flight_req['outdate']
here = flight_req['departure']
elsw = flight_req['arrival']

print('departure date: ' + lday)
print('here: ' +here)
print('there: ' +elsw)

try:
    outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder
except StaleElementReferenceException:
    print('Element not found')
    outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

lowest_out = outbound_flights[0].price

subject = 'Southwest Flights Between ' +here+ ' and ' +elsw
message = ''

for f in outbound_flights:
    if lowest_out == f.price: ####line might be unnecessary
        message = message + f.name + ' on ' +lday+ ' is available for $' + f.price + '\n'

if 'indate' in flight_req:  #return flight finder
    rday = flight_req['indate']

    try:
        inbound_flights = find_flights(elsw, here, rday)
    except StaleElementReferenceException:
        print('Element not found')
        inbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

    lowest_in = inbound_flights[0].price

    for f in inbound_flights:
        if lowest_in == f.price:
            message = message + f.name + ' on ' + rday+ ' is available for $' + f.price + '\n'

print(subject)
print(message)

sendemail(subject, message)

while not flight_day(lday):
    for i in range(12):
        print('checking again in ' +str(12-i)+ ' hours')
        time.sleep(3600)

    message = ''
    # lowoutprice = -1
    # lowinprice = -1

    if check_mail() == flight_req:
        try:
            outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder
        except StaleElementReferenceException:
            print('Element not found')
            outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

        if outbound_flights[0].price > lowest_out:
            message = message + 'The price of the ' +outbound_flights[0].name+ ' has increased! '
            message = message + 'Price has gone from ' +lowest_out+ ' to ' +outbound_flights[0].price+ '\n'
            lowest_out = outbound_flights[0].price
        elif outbound_flights[0].price < lowest_out:
            message = message + 'The price of the ' +outbound_flights[0].name+ ' has decreased! '
            message = message + 'Price has dropped from ' +lowest_out+ ' to ' +outbound_flights[0].price+ '\n'
            lowest_out = outbound_flights[0].price

        if 'indate' in flight_req:  #return flight finder
            rday = flight_req['indate']

            try:
                inbound_flights = find_flights(elsw, here, rday)
            except StaleElementReferenceException:
                print('Element not found')
                inbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

            if inbound_flights[0].price > lowest_in:
                message = message + 'The price of the ' +inbound_flights[0].name+ ' has increased! '
                message = message + 'Price has gone from ' +lowest_in+ ' to ' +inbound_flights[0].price+ '\n'
                lowinprice = inbound_flights[0].price
            elif inbound_flights[0].price < lowest_in:
                message = message + 'The price of the ' +inbound_flights[0].name+ ' has decreased! '
                message = message + 'Price has dropped from ' +lowest_in+ ' to ' +inbound_flights[0].price+ '\n'
                lowinprice = inbound_flights[0].price

        print(message)
    else:
        flight_req = check_mail()

        lday = flight_req['outdate']
        here = flight_req['departure']
        elsw = flight_req['arrival']

        print('departure date: ' + lday)
        print('here: ' +here)
        print('there: ' +elsw)

        try:
            outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder
        except StaleElementReferenceException:
            print('Element not found')
            outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

        lowest_out = outbound_flights[0].price

        subject = 'Southwest Flights Between ' +here+ ' and ' +elsw
        message = ''

        for f in outbound_flights:
            if lowest_out == f.price: ####line might be unnecessary
                message = message + f.name + ' on ' +lday+ ' is available for $' + f.price + '\n'

        if 'indate' in flight_req:  #return flight finder
            rday = flight_req['indate']

            try:
                inbound_flights = find_flights(elsw, here, rday)
            except StaleElementReferenceException:
                print('Element not found')
                inbound_flights = find_flights(here, elsw, lday) #outgoing flight finder

            lowest_in = inbound_flights[0].price

            for f in inbound_flights:
                if lowest_in == f.price:
                    message = message + f.name + ' on ' + rday+ ' is available for $' + f.price + '\n'

    sendemail(subject, message)                
#STILL TO DO
# STORE CHEAPEST FLIGHT AND UPDATE IF LOWEST PRICE CHANGES
