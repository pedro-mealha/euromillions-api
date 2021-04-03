"""
Change results table to draws table
"""

from yoyo import step

__depends__ = {'20210307_01_775A5-initial-schema'}

steps = [
    step(
        "ALTER TABLE results RENAME COLUMN contest_id TO draw_id;",
        "ALTER TABLE results RENAME COLUMN draw_id TO contest_id;"
    ),
    step(
        "ALTER INDEX results_id_uindex RENAME TO draws_id_uindex;",
        "ALTER INDEX draws_id_uindex RENAME TO results_id_uindex;"
    ),
    step(
        "ALTER INDEX results_pk RENAME TO draws_pk;",
        "ALTER INDEX draws_pk RENAME TO results_pk;"
    ),
    step(
        "ALTER TABLE results RENAME TO draws;",
        "ALTER TABLE draws RENAME TO results;"
    )
]
