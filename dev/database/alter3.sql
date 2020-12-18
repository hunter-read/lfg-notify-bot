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
    online int NOT NULL DEFAULT 0,
    nsfw int NOT NULL DEFAULT 0,
    permalink text NOT NULL, 
    PRIMARY KEY (id)
);

INSERT INTO post_new (id, date_created, date_updated, submission_id, flair, game, day, timezone, online, flag, time, permalink, nsfw)
SELECT id, 
    date_created, 
    date_updated, 
    submission_id,
    flair,
    game,
    day,
    timezone,
    CAST(online AS INTEGER) as online,
    flag,
    time,
    permalink,
    CAST(nsfw AS INTEGER) as nsfw
FROM post;

DROP TABLE post;
ALTER TABLE post_new RENAME TO post;


CREATE TABLE user_new (
    id integer NOT NULL,
    date_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username text NOT NULL,
    notification_count int NOT NULL DEFAULT 0,
    game text NOT NULL,
    day text,
    timezone text,
    nsfw int NOT NULL DEFAULT 0,
    keyword text,
    flair int NOT NULL DEFAULT 3,
    PRIMARY KEY (id)
);

INSERT INTO user_new (id, date_created, date_updated, username, notification_count, game, day, timezone, nsfw, keyword, flair)
SELECT id, 
    date_created, 
    date_updated, 
    username,
    CAST(notification_count AS INTEGER) as notification_count,
    game,
    day,
    timezone,
    CAST(nsfw AS INTEGER) as nsfw,
    keyword,
    CAST(flair AS INTEGER) as flair
FROM user;
DROP TABLE user;
ALTER TABLE user_new RENAME TO user;
