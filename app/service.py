import persistence

def get_results(year: int, dates: list):
    return persistence.get_results(year, dates)

def get_result(contest_id: int) -> list:
    return persistence.get_result_by_id(contest_id)