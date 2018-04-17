api_key='AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k'
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=api_key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Columbia University",
                                     "Time Square",
                                     mode="transit",
                                     departure_time=now,
                                     alternatives=True)

print(directions_result)

