UPDATE user set nsfw = -1 where nsfw = 0;
UPDATE user set nsfw = 0 where nsfw = 1;
ALTER TABLE user ADD COLUMN play_by_post int NOT NULL default 0;
ALTER TABLE post ADD COLUMN play_by_post int NOT NULL default 0;
UPDATE post SET play_by_post = 1 WHERE flag like '%Play-by-Post%';
ALTER TABLE user ADD COLUMN one_shot int NOT NULL default 0;
ALTER TABLE post ADD COLUMN one_shot int NOT NULL default 0;
UPDATE post SET one_shot = 1 WHERE flag like '%One-Shot%';
ALTER TABLE user ADD COLUMN lgbtq int NOT NULL default 0;
ALTER TABLE post ADD COLUMN lgbtq int NOT NULL default 0;
UPDATE post SET lgbtq = 1 WHERE flag like '%LGBTQ+%';
ALTER TABLE user ADD COLUMN age_limit int NOT NULL default 0;
ALTER TABLE post ADD COLUMN age_limit int NOT NULL default 0;
UPDATE post SET age_limit = 18 WHERE flag like '%18+%';
UPDATE post SET age_limit = 21 WHERE flag like '%21+%' or flag like '%19+%' or flag like '%20+%';
ALTER TABLE user ADD COLUMN vtt int NOT NULL default 0;
ALTER TABLE post ADD COLUMN vtt int NOT NULL default 0;
UPDATE post SET vtt = vtt + 1 WHERE flag like '%Roll20%';
UPDATE post SET vtt = vtt + 2 WHERE flag like '%Fantasy Grounds%';
UPDATE post SET vtt = vtt + 4 WHERE flag like '%Tabletop Simulator%';
UPDATE post SET vtt = vtt + 8 WHERE flag like '%Foundry VTT%';
