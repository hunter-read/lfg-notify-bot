# Developer Info
Currently made of 4 bots, one that reads incoming user messages, another that parses submissions, a scheduled service bot, and one that reads from redis and sends out notifications. The user requests are stored in a simple Sqlite database as is some post information for fun data collection.

## Requirements
### Main Codebase
* python 3.11+
* praw
* redis
* schedule

### System requirements
#### Docker
Each bot can be run in a docker container with the `python3 [submission_bot|message_bot|scheduled_bot|notification_bot].py` CMD, using the dockerfile to build the image.
Reccomend to run in a docker compose file with redis. Also needs to connect to a redis instance, either in a docker container or on the host machine.

#### Docker-Compose
A sample docker-compose is provided. By default the volume used is an external one. Create the volume and add praw.ini and the sqlite.db files to it. A sample env file is provided. This will also require adding a redis.conf file to the volume.

### Testing
* pytest (`py.test`)
* flake8 (`flake8 . --count --exit-zero --max-complexity=20  --statistics --ignore=E501`)

## Changes
If you see an issue or want to add a feature make sure there is an issue for it, and fork the repo and submit a PR for it. I usually review PR's within 24 hours but can take up to 72 hours.
