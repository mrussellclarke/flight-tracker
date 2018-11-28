from scraperfunctions import find_flights
from scraperfunctions import sendemail
# import collections
# import multiprocessing

lday = '1/23'
rday = '2/1'
here = 'LAX'
elsw = 'DTW'

outbound_flights = find_flights(here, elsw, lday) #outgoing flight finder
inbound_flights = find_flights(elsw, here, rday) #return flight finder

lowest_out = outbound_flights[0].price
lowest_in = inbound_flights[0].price

subject      = 'Southwest Flights Between ' +here+ ' and ' +elsw
message = ''

for f in outbound_flights:
    if lowest_out == f.price:
        message = message + f.name + ' on ' +lday+ ' is available for $' + f.price + '\n'

for f in inbound_flights:
    if lowest_in == f.price:
        message = message + f.name + ' on ' + rday+ ' is available for $' + f.price + '\n'

print(subject)
print(message)

sendemail(subject, message)

#STILL TO DO
#READ INCOMING EMAILS FOR FLIGHT CHECK REQUESTS
# HOST ON HEROKU
# RUN REPEATEDLY
# STORE CHEAPEST FLIGHT AND UPDATE IF LOWEST PRICE CHANGES
