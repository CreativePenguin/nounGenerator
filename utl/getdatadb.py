from datetime import datetime
from app import c
import sqlite3
import storeapi

def get_country_info_db(country):
    try:
        c.execute('''SELECT * FROM countrydata WHERE countrydata.countryname = "{}" '''.format(country))
        return c.fetchone()[0]
    except sqlite3.OperationalError:
        # This error will be returned if country is not already stored
        return storeapi.store_country_info(country)
