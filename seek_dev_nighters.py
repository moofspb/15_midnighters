import requests
from datetime import datetime
from pytz import timezone
import pytz


URL = 'https://devman.org/api/challenges/solution_attempts/'
MIDNIGHT_HOUR = 0
MORNING_HOUR = 4


def get_pages_count(url):
    page = requests.get(url)
    return page.json()['number_of_pages']


def load_attempts(url):
    first_page = requests.get(url)
    first_page_attempts = first_page.json()['records']
    pages = first_page.json()['number_of_pages']
    for attempt in first_page_attempts:
        yield attempt
    for page in range(2, pages+1):
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
            if MIDNIGHT_HOUR <= attempt_time.hour < MORNING_HOUR:
                midnighters.add(attempt['username'])
    return midnighters


def print_midnighters(url):
    attempts = load_attempts(url)
    midnighters = get_midnighters(attempts)
    print('There is {} midnighters on Devman.org:'.format(len(midnighters)))
    for i, username in enumerate(midnighters, 1):
        print(i, username)


if __name__ == '__main__':
    print_midnighters(URL)
