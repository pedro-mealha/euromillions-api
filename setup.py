import sys, requests, json, psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
from app.utils.db import Database

BASE_URL = 'https://www.euro-millions.com'
MIN_YEAR = 2004

def main(year):
    if int(year) < MIN_YEAR:
        print('{}')
        return

    parsed_results = []
    results = parsePageHtml()

    for result in results:
        data = result.find('a', class_='title')
        details_route = data['href']

        date = get_date(details_route)
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

        sql = "INSERT INTO results (numbers, stars, date, prize, has_winner) VALUES (%s, %s, %s, %s, %s);"
        db.getCursor().execute(sql, [numbers_string, stars_string, date, prize, has_winner])

    db.commit()
    db.close()
    print(json.dumps(parsed_results))

def parsePageHtml():
    url = BASE_URL + '/results-history-'+year
    page = requests.get(url)
 
    html = BeautifulSoup(page.content, 'html.parser')

    content = html.find(id='content')
    results = content.find_all('div', class_='archives')
    results.reverse() # So we insert results sorted by date ASC

    return results

def get_numbers(html):
    numbers = []
    balls = html.find_all('li', class_='new ball')
    for ball in balls: numbers.append(int(ball.text))

    return numbers

def get_stars(html):
    stars = []
    balls_star = html.find_all('li', class_='new lucky-star')
    for ball_star in balls_star: stars.append(int(ball_star.text))

    return stars

def get_date(details_route):
    date = details_route.split('/')[2]
    date = datetime.strptime(date, '%d-%m-%Y')

    return date.strftime('%Y-%m-%d')
 
def get_details(details_route):
    url = BASE_URL + details_route
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
            value = column.text.replace('Rollover! ', '').strip()
            has_winner = int(value) > 0

    return [prize, has_winner]

if __name__ == "__main__":
    year = 0
    if len(sys.argv) > 1:
        year = sys.argv[1]

    global db
    db = Database()
    main(year)
