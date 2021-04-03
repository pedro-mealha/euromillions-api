import sys, json, os
from dotenv import load_dotenv
from api import Database, external

def main(year: int) -> None:
    if int(year) < int(os.getenv("EUROMILLIONS_MIN_YEAR")):
        print('{}')
        return

    parsed_draws = []
    draws = external.get_draws_by_year(year)

    draw_id_index = 1
    for draw in draws:
        data = draw.find('a', class_='title')
        details_route = data['href']

        draw_date = external.get_date(details_route)

        date = draw_date.strftime('%Y-%m-%d')
        draw_id = str(draw_id_index) + draw_date.strftime('%Y')
        prize, has_winner = external.get_details(details_route)
        numbers = external.get_numbers(draw)
        stars = external.get_stars(draw)

        parsed_draws.append({
            "date": date,
            "prize": prize,
            "has_winner": has_winner,
            "numbers": numbers,
            "stars": stars,
        })

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        sql = "INSERT INTO draws (draw_id, numbers, stars, date, prize, has_winner) VALUES (%s, %s, %s, %s, %s, %s);"
        db.getCursor().execute(sql, [draw_id, numbers_string, stars_string, date, prize, has_winner])

        draw_id_index += 1

    db.commit()
    db.close()
    print(json.dumps(parsed_draws))

if __name__ == "__main__":
    load_dotenv()
    year = 0
    if len(sys.argv) > 1:
        year = sys.argv[1]

    global db
    db = Database()
    main(year)
