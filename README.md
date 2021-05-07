LFG Notify Bot
=============================================================================

## How to Use
[Send the bot a message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot)  with the title "Subscribe" and in the body include the following:

* Game (Required): Any game in the [LFG subreddit game tags](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags) list ("Flexible" and "Other" game tags are not supported yet)
* Timezone: Most of the Europe, North America, and Australian time zone 3 or 4 character codes are support, as is any GMT+# or UTC+# format. All timezones are converted to GMT internally, so including `EST` and `GMT-5` isn't necessary.
* Day of the Week: Monday, Tuesday, Friday, or Weekday/weekend (Most abbreviations common abbreviations are supported)
* NSFW: By default all nsfw posts are excluded, if you are okay with nsfw posts, then include "nsfw" in the message
* Specific flair: This limits flair to specific options. By default "GM and player(s) wanted" or "Player(s) wanted" are searched, but this can be limited to any of the 3 options: `GM and player(s) wanted` or `Player(s) wanted` or `GM wanted` in any combination. There is also some handy abbreviations (`gmplw`, `plw`, or `gmw` respectively) to make it a bit easier to type.
* Keywords: This is a keyword that must be included if you want a specific match (Such as a specific module name, or other flag). These must be included in square brackets "[]", and each keyword must be in it's own set of brackets. If multiple keywords are included, the bot will try and match any of them, and all keyword searches are case insensitive.   
  **Note:** Keywords are very specific, include as many as you want, including abbreviations. Keywords should also be short, you may have have better luck with a keyword such as `[strahd]` instead of `[curse of strahd]`.

Example message body
```
5e, PF2e
Monday, Wed
PST, GMT-7
```
```
40k 5E gurps
thursdays \ Friday
utc utc+1
nsfw
plw
[curse of strahd]
```

You can include as many games, timezones, or days of the week as you want and the bot will send you a message when someone posts a game looking for players that meets your criteria, but currently the bot only search for posts with [Online]. Days of week and timezone are optional, but if you do not provide this, then you may receive a multitude of messages (especially if you are looking for D&D 5e games).

### Beta features
Note these features are new and not recommended if you want a consistent experience. If you use the features below, **do so at your own risk**. You may receive incorrect notifications, or not recieve notifications for posts that match your criteria. This stuff is in testing and I guarantee nothing.   
* Offline: By default the bot only looks for online games, but now you can include `offline` to include offline games as well as online, or `=offline` for offline games only. Or use the handy abbreviations `off` and `=off` respectively. This can be included with keyword searching `[Seattle] [Washington] [WA] [Tacoma]`.

## Purpose
This is a bot that aims to make using r/lfg easier to use and provide notifications when a tabletop game that meets your criteria is posted on reddit. It can be hard to find a game that matches your schedule or plays a tabletop game that is uncommon. And unless you are lucky, have an open schedule, or are able to stalk the subreddit, it can be difficult to find a game. So I am here to help with that endeavor.

### Notes
While this bot does it's best to parse a user post, due to inconsistencies in how people post, there is no guarantee that the data it collects is 100% accurate. While the bot does try it's best, the very nature of text parsing is difficult. I recommend if you subscribe to this bot, to read through any post it thinks is applicable to your settings. If you see a blatant issue, please add an [issue to the github page](https://github.com/hunter-read/lfg-notify-bot/issues), or send [u/Perfekthuntr](https://www.reddit.com/user/Perfekthuntr) a message on reddit and I will do my best to investigate. The bot will also try and note if the post is LGBTQ+ friendly, 18+/21+, or a One-Shot and provide the game times if possible, though results may vary.

## FAQ
* **Q:** Why am I getting a notification so late after a post has been created?  
  **A:** Due to how reddit rate limits messages, the bot can currently only send 10 messages every 5 minutes. This limit changes with time and karma, which you, dear reader, can [improve by upvoting the bot a little](https://www.reddit.com/user/lfg_notify_bot).  
  
* **Q:** I sent the bot a message, but I haven't gotten any messages back, is it working?  
  **A:** When you subscribe, the bot should send a reply with your settings. Make sure you send a [**message**](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot) and **do not use** the reddit chat feature. There is also a [status page](https://stats.uptimerobot.com/KQlMrsqmqr) in case the bot goes down for some reason.
  
* **Q:** How do you set the bot to notify you of specific flairs and the Online tag?  
  **A:** Currently due to covid only games with the Online tag are included. And any post that has "Player(s) wanted" or "GM and player(s) wanted" are included. So you don't need to include that information in your message to the bot.  
  
* **Q:** Does this also work for finding in person groups?  
  **A:** Not currently. When the pandemic has begun to wane and the world returns back to normal I do plan on adding offline tag support. Until then I do not want to encourage offline play. Stay safe everyone.  
  
* **Q:** Can't you already do the same thing just by using the search tool?  
  **A:** Think of this as push notifications.  
  
* **Q:** Can the bot do \<insert feature here\>?  
  **A:** Probably not yet, but you can submit an [issue to the github page](https://github.com/hunter-read/lfg-notify-bot/issues) or [upvote features you want to see](https://www.reddit.com/user/LFG_Notify_Bot/comments/k9heax/feature_requests/) on reddit.  
  
* **Q:** How can I help?  
  **A:** Best way to do so is [submit issues](https://github.com/hunter-read/lfg-notify-bot/issues) for bugs or features. And if the bot was helpful, [leave a comment on reddit with your success story or a good/bad bot message](https://www.reddit.com/user/LFG_Notify_Bot/comments/jxsf6t/accolades_and_success_stories).  
I don't accept donations, but you can always ask your GM if they need any resources, most pour a ton of energy into the game and want everyone to have fun. Whether it be a book or artwork or maps/tokens on some VTT, support your GM in some way. Or just let them know how much fun the game is and thank them (seriously though, just saying "Thanks, that was a lot of fun, can't wait until next session" can make being a GM awesome).  
Or become a GM for a group, as the number of players overshadows the number of Game Masters. There are tons of resources for a new GM in any system and trust me when I say that it can be quite rewarding. It may seem daunting at first, but if you are honest with your players and communicate, everyone can have fun. I love the tabletop community, and want to see it grow, and this is the best way.  

* **Q:** You should make an app/website.  
  **A:** I can't do front-end ui design to save my life, unless you thought the early 90's internet looked amazing (also I hate javascript). Plus I like reddit and overall the lfg subreddit is full of good people.
  
### License
LFG Notification Bot provided under the [Simplified BSD License](https://github.com/hunter-read/lfg-notify-bot/blob/main/LICENSE)
