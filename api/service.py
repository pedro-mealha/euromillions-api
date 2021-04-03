from api import persistence, external

def get_draws(year: int, dates: list) -> list:
    return persistence.get_draws(year, dates)

def get_draw(draw_id: int) -> list:
    return persistence.get_draw_by_id(draw_id)

def parse_new_draws() -> bool:
    latest = persistence.get_latest_draw()
    if latest == None:
        return False

    latest_draw_id_parsed = int(str(latest['draw_id'])[:2])
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

        latest_draw_id_parsed += 1
        draw_id = int(str(latest_draw_id_parsed) + draw_date.strftime('%Y'))

        draws_to_insert.append([draw_id, numbers_string, stars_string, date, prize, has_winner])

    if len(draws_to_insert) > 0:
        return persistence.insert_draws(draws_to_insert)

    return True
