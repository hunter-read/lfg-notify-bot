ALTER TABLE user ADD COLUMN online int NOT NULL DEFAULT 1;
UPDATE post SET online = -1 where online = 0;