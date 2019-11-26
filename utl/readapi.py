from urllib import request
import json

country_api_link = 'https://restcountries.eu/rest/v2/'

def get_country_info(country:str, info:str) -> list:
    return json.loads(request.urlopen('https://restcountries.eu/rest/v2/name/{}'
                                      .format(country)).read())[0]['population']

print(get_country_info('China','hello'))
