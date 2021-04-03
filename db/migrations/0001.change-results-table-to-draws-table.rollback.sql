--
-- file: db/migrations/0001.change-results-table-to-draws-table.rollback.sql
-- depends: 0000.initial-schema
--

ALTER TABLE draws RENAME COLUMN draw_id TO contest_id;
ALTER INDEX draws_id_uindex RENAME TO results_id_uindex;
ALTER INDEX draws_pk RENAME TO results_pk;
ALTER INDEX draws_draw_id_uindex RENAME TO results_contest_id_uindex;
ALTER TABLE draws RENAME TO results;
