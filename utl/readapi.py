from urllib import request
import json
from dbvars import db_cursor as c

country_api_link = 'https://restcountries.eu/rest/v2/'

def get_country_info(country):
    """ Returns matrix storing name, population and so on """
    api = json.loads(request.urlopen('https://restcountries.eu/rest/v2/name/{}'
                                     .format(country)).read())[0]
    filter_api_info = {
        'name': api['name'],
        'capital': api['capital'],
        'subregion': api['subregion'],
        'population': api['population']
    }

    return api
    # return filter_api_info

def get_country_params():
    return ['name', 'capital', 'subregion', 'population']

def store_country_info():
    c.execute('something')

print(get_country_info('China'))
