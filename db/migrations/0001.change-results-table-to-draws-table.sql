--
-- file: db/migrations/0001.change-results-table-to-draws-table.sql
--

ALTER TABLE results RENAME COLUMN contest_id TO draw_id;
ALTER INDEX results_id_uindex RENAME TO draws_id_uindex;
ALTER INDEX results_pk RENAME TO draws_pk;
ALTER INDEX results_contest_id_uindex RENAME TO draws_draw_id_uindex;
ALTER TABLE results RENAME TO draws;
