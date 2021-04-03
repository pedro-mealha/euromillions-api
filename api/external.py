import os, requests
from datetime import datetime, date
from bs4 import BeautifulSoup

def get_draws_by_year(year: int) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results-history-'+year
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    content = html.find(id='content')
    draws = content.find_all('div', class_='archives')
    draws.reverse() # So we insert draws sorted by date ASC

    return draws

def get_latest_draws() -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results'
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    draws = html.find(id='content').find('tbody').find_all('tr')
    draws.reverse() # so we start to parse draws from oldest to newest

    return draws

def get_date(details_route: str) -> date:
    date_str = details_route.split('/')[2]
    parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

    return parsed_date.date()

def get_numbers(html) -> list:
    numbers = []
    balls = html.find_all('li', class_='new ball')
    for ball in balls: numbers.append(int(ball.text))

    return numbers

def get_stars(html) -> list:
    stars = []
    balls_star = html.find_all('li', class_='new lucky-star')
    for ball_star in balls_star: stars.append(int(ball_star.text))

    return stars

def get_details(details_route: str) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + details_route
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    prize = 0
    has_winner = False

    row = html.find('h2', class_='portugal').find_next('table').find('tbody').find('tr')
    if row is None:
        return [prize, has_winner]

    columns = row.find_all('td')
    for column in columns:
        if column['data-title'] == 'Prize Per Winner':
            prize = float(column.text.replace(',', '').replace('€', '').strip())
        elif column['data-title'] == 'Total Winners':
            value = column.text.replace('Rollover! ', '').replace('Rolldown! ', '').strip()
            has_winner = int(value) > 0

    return [prize, has_winner]