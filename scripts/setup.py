import json, os
import sys
from datetime import datetime
from dotenv import load_dotenv
from api import external, persistence
from api.utils.db import Database
from psycopg import sql

def main(year: int, db: Database) -> None:
    if year < int(os.getenv("EUROMILLIONS_MIN_YEAR")):
        print('{}')
        return

    parsed_draws = []
    draws = external.get_draws_by_year(year)

    prize_combinations = persistence.get_prize_combinations(db)
    combinations_ids = create_prize_combinations_dict(prize_combinations)

    draw_id_index = 1
    for draw in draws:
        draws_prizes_to_insert = []
        first_place_prize = 0

        data = draw.find('td').find('a')
        details_route = data['href']

        draw_date = external.get_date(details_route)

        date = draw_date.strftime('%Y-%m-%d')
        draw_id = str(draw_id_index) + draw_date.strftime('%Y')
        prizes, has_winner = external.get_details(details_route)
        numbers = external.get_numbers(draw)
        stars = external.get_stars(draw)

        for prize in prizes:
            if prize['combination'] == "5+2":
                first_place_prize = prize['prize']

            combination_id = combinations_ids[prize['combination']]
            draws_prizes_to_insert.append([draw_id, combination_id, prize['prize'], prize['winners']])

        numbers_string = '{' + ','.join(str(number) for number in numbers) + '}'
        stars_string = '{' + ','.join(str(star) for star in stars) + '}'

        query = sql.SQL("""
            INSERT INTO draws (draw_id, numbers, stars, date, prize, has_winner)
            VALUES ({draw_id}, {numbers}, {stars}, {date}, {prize}, {has_winner})
            ON CONFLICT (draw_id)
            DO UPDATE SET numbers = {numbers}, stars = {stars}, date = {date}, prize = {prize}, has_winner = {has_winner}
        """).format(
            draw_id=sql.Literal(draw_id),
            numbers=sql.Literal(numbers_string),
            stars=sql.Literal(stars_string),
            date=sql.Literal(date),
            prize=sql.Literal(first_place_prize),
            has_winner=sql.Literal(has_winner)
        )
        db.getConn().execute(query)

        for draws_prize in draws_prizes_to_insert:
            query = sql.SQL("""
                INSERT INTO draws_prizes (draw_id, prize_combination_id, prize, winners)
                VALUES ({draw_id}, {prize_combination_id}, {prize}, {winners})
                ON CONFLICT (draw_id, prize_combination_id)
                DO UPDATE SET prize = {prize}, winners = {winners}
            """).format(
                draw_id=sql.Literal(draws_prize[0]),
                prize_combination_id=sql.Literal(draws_prize[1]),
                prize=sql.Literal(draws_prize[2]),
                winners=sql.Literal(draws_prize[3])
            )
            db.getConn().execute(query)

        print(f'draw {draw_id} from date {date} added')

        draw_id_index += 1

    db.commit()

def create_prize_combinations_dict(prize_combinations: list):
    combinations = {}
    for prize_combination in prize_combinations:
        combination = f"{prize_combination['matched_numbers']}+{prize_combination['matched_stars']}"
        combinations[combination] = prize_combination['id']

    return combinations

if __name__ == "__main__":
    load_dotenv()
    db = Database()

    if len(sys.argv) < 2:
        current_year = datetime.now().year
        year = int(os.getenv("EUROMILLIONS_MIN_YEAR"))
        while year <= current_year:
            main(year, db)
            year += 1
    else:
        year = sys.argv[1]
        main(int(year), db)

    db.close()
