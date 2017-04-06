import requests
from datetime import datetime, time
from pytz import timezone
import pytz


URL = 'https://devman.org/api/challenges/solution_attempts/'


def get_pages_count(url):
    page = requests.get(url)
    return page.json()['number_of_pages']


def load_attempts(url):
    pages = get_pages_count(url)
    for page in range(pages):
        request = requests.get(url, {'page': page+1})
        attempts = request.json()['records']
        for attempt in attempts:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }


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
            if time(00, 00) < attempt_time.time() < time(4, 00):
                midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    attempts = load_attempts(URL)
    midnighters = get_midnighters(attempts)
    print('There is {} midnighters on Devman.org:'.format(len(midnighters)))
    for i, username in enumerate(midnighters, 1):
        print(i, username)
