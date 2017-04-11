import requests
from datetime import datetime
from pytz import timezone
import pytz


URL = 'https://devman.org/api/challenges/solution_attempts/'
FIRST_NIGHT_HOUR = 0
LAST_NIGHT_HOUR = 3


def get_pages_count(url):
    page = requests.get(url)
    return page.json()['number_of_pages']


def load_attempts(url):
    first_page = requests.get(url)
    first_page_attempts = first_page.json()['records']
    number_of_pages = first_page.json()['number_of_pages']
    for attempt in first_page_attempts:
        yield attempt
    for page in range(2, number_of_pages+1):
        request = requests.get(url, {'page': page})
        attempts = request.json()['records']
        for attempt in attempts:
            yield attempt


def get_attempt_time(attempt):
    utc = pytz.utc
    if attempt['timestamp']:
        utc_attempt_dt = utc.localize(datetime.utcfromtimestamp(attempt['timestamp']))
        return utc_attempt_dt.astimezone(timezone(attempt['timezone']))


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        attempt_time = get_attempt_time(attempt)
        if attempt_time:
            if FIRST_NIGHT_HOUR <= attempt_time.hour <= LAST_NIGHT_HOUR:
                midnighters.add(attempt['username'])
    return midnighters


def print_midnighters(midnighters):
    print('There is {} midnighters on Devman.org:'.format(len(midnighters)))
    for i, username in enumerate(midnighters, 1):
        print(i, username)


if __name__ == '__main__':
    attempts = load_attempts(URL)
    midnighters = get_midnighters(attempts)
    print_midnighters(midnighters)
