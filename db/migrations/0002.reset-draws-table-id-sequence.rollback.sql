--
-- file: db/migrations/0002.reset-draws-table-id-sequence.rollback.sql
--

ALTER SEQUENCE draws_id_seq RENAME TO results_id_seq;
