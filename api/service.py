from datetime import date
from api import persistence, external

def get_draws(year: int, dates: list) -> list:
    return persistence.get_draws(year, dates)

def get_draw(draw_id: int) -> list:
    return persistence.get_draw_by_id(draw_id)

def parse_new_draws() -> bool:
    latest = persistence.get_latest_draw()
    if latest == None:
        return False

    latest_draw_id_parsed = int(str(latest['draw_id'])[:-4])
    last_draw_date = latest['date']
    draws_to_insert = []

    latest_draws = external.get_latest_draws()

    for latest_draw in latest_draws:
        draw_data = latest_draw.find_all('td', class_='centre')
        if len(draw_data) == 0:
            continue

        draw_data.reverse() # The last <td> is the one containing the url for the details page
        draw_date_href = draw_data[0].find('a')['href']
        draw_date = external.get_date(draw_date_href)

        if draw_date <= latest['date']:
            continue

        date = draw_date.strftime('%Y-%m-%d')
        prize, has_winner = external.get_details(draw_date_href)
        numbers = external.get_numbers(latest_draw)
        stars = external.get_stars(latest_draw)

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        last_draw_date, latest_draw_id_parsed, draw_id = get_new_draw_id(last_draw_date, draw_date, latest_draw_id_parsed)

        draws_to_insert.append([draw_id, numbers_string, stars_string, date, prize, has_winner])

    if len(draws_to_insert) > 0:
        return persistence.insert_draws(draws_to_insert)

    return True

def get_new_draw_id(last_draw_date: date, current_draw_date: date, latest_draw_id: int) -> list:
    """
    This is to deal with the edge case of the end of the year, where we could be inserting
    a new draw from a new year and we need to reset the draw ID.
    """

    if current_draw_date.strftime('%Y') > last_draw_date.strftime('%Y'):
        draw_id = int('1' + current_draw_date.strftime('%Y'))
        return [current_draw_date, 1, draw_id]

    latest_draw_id += 1
    draw_id = int(str(latest_draw_id) + current_draw_date.strftime('%Y'))
    return [current_draw_date, latest_draw_id, draw_id]
