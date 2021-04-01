"""
Initial schema
"""

from yoyo import step

steps = [
    step(
        """
        CREATE TABLE results
        (
            id SERIAL NOT NULL,
            contest_id INT NOT NULL,
            numbers TEXT[] NOT NULL,
            stars TEXT[] NOT NULL,
            date DATE NOT NULL,
            prize FLOAT DEFAULT 0,
        has_winner BOOLEAN DEFAULT false
        );
        """,
        "DROP TABLE results"
    ),
    step(
        "CREATE UNIQUE INDEX results_id_uindex ON results (id);",
        "CREATE UNIQUE INDEX results_contest_id_uindex ON results (contest_id);"
    ),
    step("ALTER TABLE results ADD CONSTRAINT results_pk PRIMARY KEY (id);")
]
