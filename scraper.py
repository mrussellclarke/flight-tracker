from scraperfunctions import find_flights, check_mail, sendemail
# import collections
# import multiprocessing

flight_req = check_mail()

lday = flight_req['outdate']
here = flight_req['departure']
elsw = flight_req['arrival']

print('departure date: ' + lday)
print('here: ' +here)
print('there: ' +elsw)

outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder
lowest_out = outbound_flights[0].price

subject      = 'Southwest Flights Between ' +here+ ' and ' +elsw
message = ''

for f in outbound_flights:
    if lowest_out == f.price:
        message = message + f.name + ' on ' +lday+ ' is available for $' + f.price + '\n'

if 'indate' in flight_req:  #return flight finder
    rday = flight_req['backdate']
    inbound_flights = find_flights(elsw, here, rday)

    lowest_in = inbound_flights[0].price

    for f in inbound_flights:
        if lowest_in == f.price:
            message = message + f.name + ' on ' + rday+ ' is available for $' + f.price + '\n'

print(subject)
print(message)

# sendemail(subject, message)

#STILL TO DO
#READ INCOMING EMAILS FOR FLIGHT CHECK REQUESTS
# RUN REPEATEDLY
# STORE CHEAPEST FLIGHT AND UPDATE IF LOWEST PRICE CHANGES
