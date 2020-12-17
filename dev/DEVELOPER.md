# Developer Info
Currently made of 2 bots, one that reads incoming user messages and another that parses and notifies users on submissions. The user requests are stored in a simple Sqlite database as is some post information for fun data collection.

## Requirements
### Main Codebase
* python 3.7+
* praw
* redis
* schedule

### System requirements
I have only tested this on Ubuntu and MacOS. Any other operating system may not be supported or have behavior issues.
* [Redis](https://redis.io/topics/quickstart) is required on your system or docker container. The advantages of migrating to redis, is that app level restarts have less impact on production and allows me to easily decouple things.

### Testing
* pytest (`py.test`)
* flake8 (`flake8 . --count --exit-zero --max-complexity=10  --statistics --ignore=E501`)

## Changes
If you see an issue or want to add a feature make sure there is an issue for it, and fork the repo and submit a PR for it. I usually review PR's within 24 hours but can take up to 72 hours.
