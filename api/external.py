import os, requests
from datetime import datetime, date
from bs4 import BeautifulSoup

def get_draws_by_year(year: int) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results-history-'+ str(year)
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    content = html.find(id='content')
    draws = content.find('tbody').find_all('tr', class_='resultRow')
    draws.reverse() # So we insert draws sorted by date ASC

    return draws

def get_latest_draws() -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results'
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    draws = html.find(id='content')

    return draws

def get_date(details_route: str) -> date:
    date_str = details_route.split('/')[2]
    parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

    return parsed_date.date()

def get_numbers(html) -> list:
    numbers = []
    balls = html.find_all('li', class_='ball')
    if balls[0].text == '-':
        return numbers

    for ball in balls: numbers.append(int(ball.text))

    return numbers

def get_stars(html) -> list:
    stars = []
    balls_star = html.find_all('li', class_='lucky-star')
    if balls_star[0].text == '-':
        return stars

    for ball_star in balls_star: stars.append(int(ball_star.text))

    return stars

def get_details(details_route: str) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + details_route
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    prizes = []
    has_winner = False

    body = html.find(id="PrizePT")
    body = body if body is not None else html.find(id="PrizeES")
    if body is None:
        return [prizes, has_winner]

    rows = body.find('tbody').find_all('tr')
    if len(rows) == 0:
        return [prizes, has_winner]

    for row in rows:
        if row.find('td').text.replace(' ', '').strip() == 'Totals':
            continue

        prize = {
            "prize": 0,
            "winners": 0,
            "combination": ""
        }

        columns = row.find_all('td')
        for column in columns:
            if column['data-title'] == 'Numbers Matched':
                value = column.text.replace(' ', '').strip()
                if len(value) == 1:
                    value = f"{value}+0"
                prize['combination'] = value
            elif column['data-title'] == 'Prize Per Winner':
                prize['prize'] = float(column.text.replace(',', '').replace('€', '').strip())
            elif column['data-title'] == 'Total Winners':
                prize['winners'] = column.text.replace(',', '').replace('Rollover! ', '').replace('Rolldown! ', '').strip()

        if prize['combination'] == "5+2" and int(prize['winners']) > 0:
            has_winner = True

        prizes.append(prize)

    return [prizes, has_winner]
