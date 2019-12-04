from urllib import request
import json
import random
import html


COUNTRY_API_LINK = 'https://restcountries.eu/rest/v2/'
TRIVIA_API_TOKEN_LINK = 'https://opentdb.com/api_token.php'
TRIVIA_API_LINK = 'https://opentdb.com/api.php'


def get_country_info(country):
    """Returns matrix storing name, population and so on"""
    # api = json.loads(request.urlopen('https://restcountries.eu/rest/v2/name/{}'
    #                                  .format(country)).read())[0]
    api = json.loads(request.urlopen('{}name/{}'.format(COUNTRY_API_LINK,
                                                        country)).read())[0]
    filter_api_info = {
        'countryname': api['name'],
        'capital': api['capital'],
        'subregion': api['subregion'],
        'population': api['population'],
        'demonym': api['demonym'],
        'flag': api['flag'],
        'languages': api['languages']
    }

    # return api
    return filter_api_info


def get_country_params():
    """Stores the api parameters used to make trivia questions"""
    return ['countryname', 'population', 'capital', 'subregion', 'population']

"""
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
"""

def trivia_questions(apitoken=None):
    """Returns all the trivia questions to be displayed"""
    data = {}
    if apitoken == None:
        data = json.loads(request.urlopen('{}?amount=10'
                                          .format(TRIVIA_API_LINK)).read())
    else:
        data = json.loads(request.urlopen('{}?amount=10&token={}'
                                          .format(TRIVIA_API_LINK,
                                                  apitoken)).read())
    if data['response_code'] == 4:
        request.urlopen('{}?command=reset&token={}'
                        .format(TRIVIA_API_TOKEN_LINK, apitoken))
        trivia_questions(apitoken)
    val = []  # Collects the val of [question #, question, ans1, ans2, ans3, ans4, index of right ans]
    answers = []  # Stores all of the potential answers in a separate array to scramble them
    tmp = []  # Holds val in an arr of arrs
    for i in range(10):
        val.append(i + 1)
        val.append(html.unescape(data['results'][i]['question']))
        for j in data['results'][i]['incorrect_answers']:
            answers.append(j)
        answers.append(data['results'][i]['correct_answer'])
        if 'True' in answers:
            answers.append('-1')
            answers.append('-1')
        if 'True' not in answers:
            random.shuffle(answers)
        for j in answers:
            val.append(j)
        val.append(answers.index(data['results'][i]['correct_answer']))
        answers = []
        tmp.append(val)
        val = []
    return tmp


def trivia_apitoken():
    """Returns a new api token for trivia to keep the trivia questions fresh
    Each token will always get new questions, each user should have a token
    """
    data = json.loads(request.urlopen('{}?command=request'
                                      .format(TRIVIA_API_TOKEN_LINK)).read())
    if data['response_code'] != 0:
        # TODO: Handle this exception boi!
        return Exception
    return data['token']

# print(get_country_info('China'))
# print(get_country_info('Germany'))
# print(store_country_info('China'))
