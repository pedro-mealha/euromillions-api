"""
Change results table to draws table
"""

from yoyo import step

__depends__ = {'20210307_01_775A5-initial-schema'}

steps = [
    step("ALTER TABLE results RENAME TO draws;"),
    step("ALTER TABLE results RENAME COLUMN contest_id TO draw_id;")
]
