# Weekly changelog
This changelog will be updated monthly (or whenever I have time) to include any changes that have occured. Any changes made may have been included in hotfixes in between versions, and some features may not be live for all users.



## Version 1.4.0 - April 13th, 2021
Added a host of new features for beta testing.
* Added offline support.
* Added pbp, vtt, and other flag support.
* Notification bot fixes.
* Refactored Readme to improve readability.
* Upgrade to python 3.8+ (3.7 no longer supported)

## Version 1.3.0 - April 13th, 2021
This is an internal set of changes for ease of my life.
* Added docker support
* Updated some environment support.

## Version 1.2.2 - Jan 29th, 2021
Bug fixes
* Keyword filter moved to stable

## Version 1.2.1 - Dec 24th, 2020
Squashed more bugs
* Fixed user search timezone bug again
* Added flair shorthand
* Flair filter moved to stable

## Version 1.2.0 - Dec 18th, 2020
Added beta testing for a handful of new features and some bug fixes
* Keyword search added
* Flair filters added
* Added support to identify play by post 

## Version 1.1.0 - Dec 8th, 2020
Major changes to how messages are sent to improve scalibilty and reliability
* Rewrote and broke apart submission and notifications
* Improved scalibilty with redis
* Small bug fixes to ratelimits

## Version 1.0.1 - Dec 5th, 2020
Called an exterminator to deal with bugs. (Bug fixes and stability improvements.)
* Removed WEST timezone due to parsing issues.
* Fixed GMT+-1 searching flaging incorrect timezones.
* Improved bot messaging with users.
* Ratelimit handling improvements.
* Readme updates.
* Other bug fixes that I'm too lazy to document because this is a hobby project and I doubt anyone will read this.
* Probably added some bugs to fix later.

## Version 1.0.0 - Dec 1st, 2020
Initial Release
* Basic support for Online, Looking for Player(s) submissions to r/LFG
* User filter support for games, timezone, day of week, and nsfw filters.
