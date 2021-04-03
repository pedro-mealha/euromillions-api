import sys, requests, json, os
from datetime import datetime

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from app.utils.db import Database

def main(year: int) -> None:
    if int(year) < int(os.getenv("EUROMILLIONS_MIN_YEAR")):
        print('{}')
        return

    parsed_results = []
    results = parsePageHtml()

    contest_id_index = 1
    for result in results:
        data = result.find('a', class_='title')
        details_route = data['href']

        contest_datetime = get_date(details_route)

        date = contest_datetime.strftime('%Y-%m-%d')
        contest_id = str(contest_id_index) + contest_datetime.strftime('%Y')
        prize, has_winner = get_details(details_route)
        numbers = get_numbers(result)
        stars = get_stars(result)

        parsed_results.append({
            "date": date,
            "prize": prize,
            "has_winner": has_winner,
            "numbers": numbers,
            "stars": stars,
        })

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        sql = "INSERT INTO results (contest_id, numbers, stars, date, prize, has_winner) VALUES (%s, %s, %s, %s, %s, %s);"
        db.getCursor().execute(sql, [contest_id, numbers_string, stars_string, date, prize, has_winner])

        contest_id_index += 1

    db.commit()
    db.close()
    print(json.dumps(parsed_results))

def parsePageHtml() -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results-history-'+year
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    content = html.find(id='content')
    results = content.find_all('div', class_='archives')
    results.reverse() # So we insert results sorted by date ASC

    return results

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

def get_date(details_route: str) -> datetime:
    date = details_route.split('/')[2]
    date = datetime.strptime(date, '%d-%m-%Y')

    return date

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

if __name__ == "__main__":
    year = 0
    if len(sys.argv) > 1:
        year = sys.argv[1]

    load_dotenv()
    global db
    db = Database()
    main(year)
