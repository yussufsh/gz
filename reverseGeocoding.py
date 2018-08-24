import requests


def reverse_geocode(lat,lon):
    # Did the geocoding request comes from a device with a
    # location sensor? Must be either true or false.
    sensor = 'true'

    # Hit Google's reverse geocoder directly
    # NOTE: I *think* their terms state that you're supposed to
    # use google maps if you use their api for anything.
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=lat,
        lon=lon,
        sen=sensor
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()


def get_taluka(lat,lon):
    toReturn = {}
    response = reverse_geocode(lat,lon)
    #toReturn['full_address'] = response['results'][0]['formatted_address']
    for result in response['results']:
        for component in result['address_components']:
            if 'administrative_area_level_3' in component['types']:
                toReturn['taluka'] = component['long_name']
            elif 'route' in component['types']:
                toReturn['full_address'] = component['long_name']		
            elif 'locality' in component['types']:
                toReturn['city'] = component['long_name']
            elif 'administrative_area_level_1' in component['types']:
                toReturn['state'] = component['long_name']
    return toReturn

print(get_taluka(15.366,73.934))
