from urllib import request
import json
from dbvars import db_cursor as c

def get_country_info(country):
    """ Returns matrix storing name, population and so on """
    api = json.loads(request.urlopen('https://restcountries.eu/rest/v2/name/{}'
                                     .format(country)).read())[0]
    filter_api_info = {
        'countryname': api['name'],
        'capital': api['capital'],
        'subregion': api['subregion'],
        'population': api['population'],
        'demonym': api['demonym'],
        'flag':api['flag'],
        'languages':api['languages']
    }

    return api
    # return filter_api_info

def get_country_params():
    return ['countryname', 'population', 'capital', 'subregion', 'population']

def store_country_info(country):
    api_info = get_country_info(country)
    c.execute("SELECT owner FROM countrydata WHERE countrydata.countryname = {}".format(country))
    api_info['owner'] = c.fetchone()[0]
    c.execute('''INSERT INTO countrydata VALUES (
"{countryname}",
"{population}",
"{capital}",
"{demonym}",
"{flag_url}",
"{languages}",
"{owner}");'''.format(**api_info))
    return api_info['owner']

# print(get_country_info('China'))
# print(get_country_info('Germany'))
# print(store_country_info('China'))
