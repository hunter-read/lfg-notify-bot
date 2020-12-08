ALTER TABLE user_request ADD COLUMN notification_count int DEFAULT 0;
ALTER TABLE user_request ADD COLUMN game_json JSON;

SELECT * from user_request order by date_created desc;