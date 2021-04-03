--
-- file: db/migrations/0002.reset-draws-table-id-sequence.sql
-- depends: 0000.initial-schema 0001.change-results-table-to-draws-table
--

ALTER SEQUENCE results_id_seq RENAME TO draws_id_seq;
ALTER SEQUENCE draws_id_seq RESTART;

UPDATE draws SET id = DEFAULT;
