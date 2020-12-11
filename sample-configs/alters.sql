CREATE TABLE post_new (
    id integer NOT NULL,
    date_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submission_id text NOT NULL,
    flair text,
    game text,
    day text,
    timezone text,
    flag text,
    time text,
    online int NOT NULL DEFAULT '0',
    nsfw int NOT NULL DEFAULT '0',
    permalink text NOT NULL, 
    PRIMARY KEY (id)
);

INSERT INTO post_new (id, date_created, date_updated, submission_id, flair, game, day, timezone, online, flag, time, permalink, nsfw)
SELECT id, 
    post_date as date_created, 
    post_date as date_updated, 
    COALESCE(submission_id, '') AS submission_id,
    flair,
    game,
    days as day,
    timezone,
    online,
    flag,
    times as time,
    permalink,
    nsfw
FROM post;

DROP TABLE post;
ALTER TABLE post_new RENAME TO post;


DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id integer NOT NULL,
    date_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username text NOT NULL,
    notification_count int NOT NULL DEFAULT '0',
    game text NOT NULL,
    day text,
    timezone text,
    nsfw int NOT NULL DEFAULT '0',
    start_time_min int,
    start_time_max int,
    keyword text,
    PRIMARY KEY (id)
);

INSERT INTO user (id, date_created, date_updated, username, notification_count, game, day, timezone, nsfw)
SELECT id, 
    date_created, 
    date_created as date_updated, 
    username,
    notification_count,
    game,
    day_of_week as day,
    timezone,
    nsfw
FROM user_request;
DROP TABLE user_request;
