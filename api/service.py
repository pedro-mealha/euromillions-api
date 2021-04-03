import os, requests

from bs4 import BeautifulSoup

import api.persistence as persistence
import api.external as external

def get_results(year: int, dates: list) -> list:
    return persistence.get_results(year, dates)

def get_result(contest_id: int) -> list:
    return persistence.get_result_by_id(contest_id)

def parse_new_results() -> bool:
    latest = persistence.get_latest_result()
    if latest == None:
        return False

    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results'
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    latest_contest_id_parsed = int(str(latest['contest_id'])[:2])

    contests = []
    results = html.find(id='content').find('tbody').find_all('tr')
    results.reverse() # so we start to parse contests from oldest to newest
    for result in results:
        result_data = result.find_all('td', class_='centre')
        if len(result_data) == 0:
            continue

        result_data.reverse() # The last <td> is the one containing the url for the details page
        result_date_href = result_data[0].find('a')['href']
        result_date = external.get_date(result_date_href)

        if result_date <= latest['date']:
            continue

        date = result_date.strftime('%Y-%m-%d')
        prize, has_winner = external.get_details(result_date_href)
        numbers = external.get_numbers(result)
        stars = external.get_stars(result)

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        latest_contest_id_parsed += 1
        contest_id = int(str(latest_contest_id_parsed) + result_date.strftime('%Y'))

        contests.append([contest_id, numbers_string, stars_string, date, prize, has_winner])

    if len(contests) > 0:
        return persistence.insert_contests(contests)

    return True
