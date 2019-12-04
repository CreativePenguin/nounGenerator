""" Contians methods for reading and storying the apis """
from urllib import request
import json
from dbvars import db_cursor as c
import sqlite3
from datetime import datetime


def get_country_info_api(country):
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
    """ Returns the various fields we use to make questions """
    return ['countryname', 'population', 'capital', 'subregion', 'population']


def store_country_info(country):
    """ Stores general country info into datatable so we don't need to access api"""
    api_info = get_country_info_api(country)
    try:
        c.execute('''SELECT countrydata.owner FROM countrydata
                     WHERE countrydata.countryname = "{}" '''.format(country))
        api_info['owner'] = c.fetchone()[0]
    except sqlite3.OperationalError:
        # This error will be returned if api info about country is not already stored
        api_info['owner'] = ""
    api_info['lastaccessed'] = datetime.time().now()
    c.execute('''INSERT INTO countrydata VALUES (
"{countryname}",
"{population}",
"{capital}",
"{demonym}",
"{flag_url}",
"{languages}",
"{owner}",
"{lastaccessed}");'''.format(**api_info))
    return api_info

# j = store_country_info('China')
# for i in j.keys():
#     print(j[i])
print(get_country_info_api('China'))
# print(get_country_info('Germany'))
# print(store_country_info('China'))
