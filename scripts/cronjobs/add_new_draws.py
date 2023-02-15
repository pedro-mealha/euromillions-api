from datetime import date
from dotenv import load_dotenv

def main() -> None:
    latest = persistence.get_latest_draw()
    if latest == None:
        return print('latest draw not found')

    latest_draw_id_parsed = int(str(latest['draw_id'])[:-4])
    last_draw_date = latest['date']
    draws_to_insert = []

    latest_draws = external.get_latest_draws()
    draws = latest_draws.find('tbody').find_all('tr', class_='resultRow')
    draws.reverse()
    last_two_draws = latest_draws.find('div', class_='fx wrapSM').find_all('div', recursive=False);
    draws.append(last_two_draws[1])
    draws.append(last_two_draws[0])

    for draw in draws:
        if len(draw) == 0:
            continue

        draw_date_href = draw.find('a')['href']
        draw_date = external.get_date(draw_date_href)

        if draw_date <= latest['date']:
            continue

        date = draw_date.strftime('%Y-%m-%d')
        prize, has_winner = external.get_details(draw_date_href)
        numbers = external.get_numbers(draw)
        if len(numbers) == 0:
            continue

        stars = external.get_stars(draw)
        if len(stars) == 0:
            continue

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        last_draw_date, latest_draw_id_parsed, draw_id = get_new_draw_id(last_draw_date, draw_date, latest_draw_id_parsed)

        draws_to_insert.append([draw_id, numbers_string, stars_string, date, prize, has_winner])
        print(f'draw from {date} to be added')

    if len(draws_to_insert) > 0:
        print(f'{len(draws_to_insert)} draws added')
        return persistence.insert_draws(draws_to_insert)

    print('no new draws to add')

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

if __name__ == "__main__":
    load_dotenv()

    from api import persistence, external
    main()
