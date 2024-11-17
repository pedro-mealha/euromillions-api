-- add-prizes-tables
-- depends: 0002.reset-draws-table-id-sequence

CREATE TABLE prize_combinations (
    id SERIAL NOT NULL,
    matched_numbers INT NOT NULL,
    matched_stars INT NOT NULL
);

CREATE UNIQUE INDEX prize_combinations_id_uindex ON prize_combinations (id);
ALTER TABLE prize_combinations ADD CONSTRAINT prize_combinations_pk PRIMARY KEY (id);


CREATE TABLE draws_prizes (
    draw_id INT NOT NULL,
    prize_combination_id INT NOT NULL,
    prize FLOAT NOT NULL,
    winners INT DEFAULT 0
);

CREATE UNIQUE INDEX draws_prizes_draw_id_prize_combination_id_uindex ON draws_prizes (draw_id, prize_combination_id);
ALTER TABLE draws_prizes ADD CONSTRAINT draws_prizes_draws_id_fk FOREIGN KEY (draw_id) REFERENCES draws (draw_id);
ALTER TABLE draws_prizes ADD CONSTRAINT draws_prizes_prize_combinations_id_fk FOREIGN KEY (prize_combination_id) REFERENCES prize_combinations (id);
