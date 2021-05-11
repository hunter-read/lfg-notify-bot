LFG Notify Bot
=============================================================================

## How to Use
[Send the bot a message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot&subject=Subscribe) with the subject **"Subscribe"** and in the message include the following information:

| Information | Example | Description |
| --- | --- | --- |
| **Game** (Required) | `5e`, `PF2E`, `coc` | Any game in the [LFG subreddit game tags](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags) list ("Flexible" and "Other" game tags are not supported yet) |
| Timezone | `EST`, `GMT-5` `UTC` | Most of the Europe, North America, and Australian time zone 3 or 4 character codes are support, as is any GMT+#. | 
| Day of Week | `Monday`, `tues`, or `weekends` | Any day of the week can be provided: Monday, Tuesday, Wednesday, ..., Sunday or `Weekday`/`weekend` (Most abbreviations common abbreviations are supported) |
| Keywords | `[strahd]` `[Pittsburg]` `[star wars]`| This is a case insensitive keyword that must be included if you want a specific match (Such as a specific module name, or other flag). These must be included in square brackets "[]", and each keyword must be in it's own set of brackets. If multiple keywords are included, the bot will try and match any of them.|

### Basic Example Message Body
```
5e, PF2e
Monday, Wed
PST, GMT-7
```
or 
```
5E EST Weekends
[curse of strahd] [strahd] [cos]
```

### Notes
* **By default only online, non-nsfw, and "GM and player(s) wanted" or "Player(s) wanted" flaired posts are matched.**
* You can include as many *games*, *timezones*, *days of the week*, *keywords* as you want and the bot will send you a message when someone posts a game looking for players that meets your criteria. 
* If using *keywords*, keep them short and use abbreviations if they exist. Instead of just using `[curse of strahd]`,  also use `[strahd]` and `[cos]`. More is usually better.

------

## Advanced Options
*Beta features are still in testing, and may provide inconsistent results. Use at your own risk.*
| Information | Options | Description |
| --- | --- | --- |
| Specific flair | GM & player's: `gmplw`<br/>Player's wanted: `plw`<br/>GM wanted: `gmw` | By default "GM and player(s) wanted" or "Player(s) wanted" are searched, but this can be limited to any of the 3 options |
| NSFW | Include: `nsfw`<br/>Only:`=nsfw` | By default all nsfw posts are excluded, if you are okay with nsfw posts, then include `nsfw` and if you only want nsfw then include `=nsfw`. |
| *Offline* (Beta) | Include: `offline` (`off`)<br/>Only: `=offline` (`=off`) | By default the bot only looks for online games, but now you can include `offline` to include offline and online games, or `=offline` for only offline. |
| *Identity* (Beta) | LGBTQ+: `lgbtq`<br/> Feminine or Woman: `fem`<br/>People of Color: `poc`<br/>Accessible: `accessible` | Several identity tags have been made available for users who may have a harder time than most making a group of people, these flags then include only posts that explicitly mention identity. |
| *Age* (Beta) | `anyage`, `18+`, or `21+` | `anyage` searches for posts with no given age limit. `18+`, and `21+` search for games labeled as such. (Note 21+ includes any games labeled 18+ as well) |
| *Play by Post* (Beta) | Only: `=pbp`<br/>Exclude: `-pbp` | Include only play-by-post games with `pbp` and exclude all play-by-post games with `-pbp`. |
| *One-shot* (Beta) | Only: `=oneshot`<br/>Exclude: `-oneshot` | Include only one-shot games with `oneshot` and exclude all one-shot games with `-oneshot`. |
| *Virtual Table Top* (Beta) | Roll20: `roll20`<br/>Fantasy Grounds: `fg`<br/>Tabletop Simulator: `tts`<br/>Foundry VTT: `foundry` | Include only games that expressly mention the VTT. Want to add another VTT? [Message me](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=Add%20New%20VTT%20to%20LFG%20Notification%20Bot) |


## Advanced Example message body

```
40k 5E gurps
thursdays \ Friday
utc utc+1
nsfw plw offline 21+
-pbp -oneshot
roll20
[atlanta]
```
----

## Purpose
This is a bot that aims to make using r/lfg easier to use and provide notifications when a tabletop game that meets your criteria is posted on reddit. It can be hard to find a game that matches your schedule or plays a tabletop game that is uncommon. And unless you are lucky, have an open schedule, or are able to stalk the subreddit, it can be difficult to find a game. So I am here to help with that endeavor.

### Notes
While this bot does it's best to parse a user post, due to inconsistencies in how people post, there is no guarantee that the data it collects is 100% accurate. While the bot does try it's best, the very nature of text parsing is difficult. I recommend if you subscribe to this bot, to read through any post it thinks is applicable to your settings. If you see a blatant issue, please add an [issue to the github page](https://github.com/hunter-read/lfg-notify-bot/issues), or [send me](https://www.reddit.com/user/Perfekthuntr) a message on reddit and I will investigate.

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

* **Q:** You should make an app/website.  
  **A:** I can't do front-end ui design to save my life, unless you thought the early 90's internet looked amazing (also I hate javascript). Plus I like reddit and overall the lfg subreddit is full of good people.
  
### License
LFG Notification Bot provided under the [Simplified BSD License](https://github.com/hunter-read/lfg-notify-bot/blob/main/LICENSE)
