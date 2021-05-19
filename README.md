LFG Notify Bot
=============================================================================
<p align="center">
  <a href="https://www.python.org/downloads/release/python-380/" target="_blank">
    <img src="https://img.shields.io/badge/python-v3.8%2B-blue" alt="python-version">
  </a>
  <a href="https://github.com/hunter-read/lfg-notify-bot/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/hunter-read/lfg-notify-bot/actions/workflows/test.yml/badge.svg" alt="github action status">
  </a>
  <a href="https://hub.docker.com/repository/docker/hunterreadca/lfg-notify-bot" target="_blank">
    <img src="https://img.shields.io/docker/image-size/hunterreadca/lfg-notify-bot/stable" alt="docker">
  </a>
  <br>
  <a href="https://github.com/hunter-read/lfg-notify-bot/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/hunter-read/lfg-notify-bot" alt="license">
  </a>
  <a href="https://stats.uptimerobot.com/KQlMrsqmqr" target="_blank">
    <img src="https://img.shields.io/uptimerobot/ratio/m786376456-4d6cc003c3e5f06efeb0a058" alt="uptime">
  </a>
  <a href="https://github.com/hunter-read/lfg-notify-bot/commits/main" target="_blank">
    <img src="https://img.shields.io/github/last-commit/hunter-read/lfg-notify-bot/main" alt="uptime">
  </a>
  
</p>

This is a bot that aims to make using [r/lfg](https://www.reddit.com/r/lfg/) easier to use and provide notifications when a tabletop game that meets your criteria is posted on reddit. It can be hard to find a game that matches your schedule or plays a tabletop game that is uncommon. And unless you are lucky, have an open schedule, or are able to endlessly scroll the subreddit, it can be difficult to find a game. So this bot is here to help.

<h2 align="center"> >>> There is <a href="https://readpnw.dev/lfg" target="_blank">now a web page to subscribe</a> to the bot easily <<< </h2>

# How to Use

[Send the bot a message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot&subject=Subscribe) with the subject **"Subscribe"** and in the message include the information below.  
**Note**: Only *game* is **required**, everything else is optional.

| Information | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example/Options&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
| --- | --- | --- |
| **Game** (Required) | `5e`, `PF2E`, `coc`, `flexible` | Any game in the [LFG subreddit game tags](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags) list ("Flexible" and "Other" game tags use `flexible`) |
| Timezone | `EST`, `GMT-5`, `UTC`, `gmt+10:30` | Most of the Europe, North American, and Australian 3 or 4 character codes are support, as is any GMT+#. Posts missing timezone information can still be included with `no-tz` if other timezones are included in your filters. [Timezone Help](https://www.timeanddate.com/time/map/) | 
| Day of Week | `Monday` or`mon`,<br/>and/or `tues`,<br/>and/or `weekends` | Any day of the week can be provided: Monday, Tuesday, ..., Sunday (Most abbreviations are supported). Posts missing day of week information can still be included with `no-day` if other days are included in your filters.|
| Keywords | `[strahd]`<br/>`[New york]`<br/>`[star wars]`| This is a case insensitive text that must be included if you want a to filter on something specific. These must be included in square brackets "[]", and each keyword must be in it's own set of brackets. |
| Specific flair | GM & player's: `gmplw`<br/>Player's wanted: `plw`<br/>GM wanted: `gmw` | By default "GM and player(s) wanted" or "Player(s) wanted" are searched, but this can be limited to any of the 3 options |
| NSFW | Include: `nsfw`<br/>Only: `=nsfw` | By default all nsfw posts are excluded, if you are okay with nsfw posts, then include `nsfw` and if you only want nsfw then include `=nsfw`. |
| Location Type | Include: `offline` (`off`)<br/>Only: `=offline` (`=off`) | By default the bot only looks for online games, but you can include `off` to include offline and online games, or `=off` for only offline. |
| Identity | LGBTQ+: `lgbtq`<br/> Feminine or Woman: `fem`<br/>People of Color: `poc`<br/>Accessible: `accessible` | Several identity tags have been made available for users who may have a harder time than most making a group of people, these flags then include only posts that explicitly mention identity. |
| Age | Not age gated: `anyage`<br/>18 and older: `18+`<br/>21 and older: `21+`| `anyage` excludes age gated games. `18+`, and `21+` search for games labeled as such. (Note 21+ includes any games labeled 18+ as well) |
| Play by Post | Only: `=pbp`<br/>Exclude: `-pbp` | Include only play-by-post games with `pbp` and exclude all play-by-post games with `-pbp`. |
| One-shot | Only: `=oneshot`<br/>Exclude: `-oneshot` | Include only one-shot games with `oneshot` and exclude all one-shot games with `-oneshot`. |
| Virtual Tabletop | [Roll20](https://roll20.net/welcome): `roll20`<br/>[Fantasy Grounds](https://www.fantasygrounds.com/home/home.php): `fg`<br/>[Tabletop Simulator](https://www.tabletopsimulator.com/): `tts`<br/>[Foundry VTT](https://foundryvtt.com/): `foundry`<br/>[Astral Tabletop](https://www.astraltabletop.com/): `astral`<br/>[TablePlop](https://new.tableplop.com/): `tableplop`<br/>[TaleSpire](https://talespire.com/): `talespire` | Include only games that expressly mention a Virtual Tabletop (VTT). Not recommended when looking for offline games. <br/>Want to add another VTT? [Message the developer](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=Add%20New%20VTT%20to%20LFG%20Notification%20Bot) |

### Message Body Examples
```
CoC, PF2e
Monday, Wed
PST, GMT-7
```
or 
```
5E EST Weekends
[curse of strahd] [strahd] [cos]
```
or
```
40k 5E gurps
thursdays \ Friday
gmt gmt+1
nsfw plw offline 21+ lgbtq
-pbp -oneshot
[seattle] [bellevue] [WA]
```

## Notes / Tips
* **By default** only *online*, *non-nsfw*, and "GM and player(s) wanted" or "Player(s) wanted" *flaired* posts are matched.
* You can include as many *games*, *timezones*, *days of the week*, *keywords* as you want and the bot will send you a message when someone posts a game looking for players that meets your criteria. 
* If using *keywords*, keep them short and use abbreviations if they exist. Instead of just using `[curse of strahd]`,  also use `[strahd]` and `[cos]`. More is usually better, as keywords match any of your inputs. 
* It's **NOT** recommended to include *keywords* used by other options, such as *identity*, *vtt*, or any other option.
* **Don't** include every *day of the week*, every *timezone*, or all *vtt* options. By default all options are included, these are meant to filter down the notifications.
* The bot provides many filters, but you don't need to use them all, pick the ones that you care about most. Too many options, and the bot won't find any posts, but too few (especially for D&D 5th Edition) and you may get too many.


### Disclaimer
While this bot does it's best to parse a user post, due to inconsistencies in how people post, there is no guarantee that the data it collects is 100% accurate. While the bot does try it's best, the very nature of text parsing is difficult. If you subscribe to this bot, make sure to read through any post the bot thinks is applicable to your filters.

If you see a blatant issue, please add an [issue to the github page](https://github.com/hunter-read/lfg-notify-bot/issues), or [send the developer](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue) a message on reddit.


## FAQ
* **Q:** Why am I getting a notification so late after a post has been created?  
  **A:** Due to how reddit rate limits messages, the bot can only send 10 messages every 5 minutes. This limit changes with time and karma.  
  
* **Q:** I sent the bot a message, but I haven't gotten any messages back, is it working?  
  **A:** When you subscribe, the bot should send a reply with your settings. Make sure you send a [**message**](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot&subject=Subscribe) and **do not use** the reddit chat feature. There is also a [status page](https://stats.uptimerobot.com/KQlMrsqmqr) to see if the bot is down for some reason.
  
* **Q:** How do you set the bot to notify you of specific flairs and the Online tag?  
  **A:** See the *Specific flair* filter option. By default all online tagged posts are included.
  
* **Q:** Does this also work for finding in person groups?  
  **A:** Yes, see the *Location Type* filter option above. This can be combined with keyword searching to limit to a specific city, state, province, or other location information.
  
* **Q:** Can't you already do the same thing just by using the search tool?  
  **A:** Think of this as push notifications.  
  
* **Q:** Can the bot do \<insert feature here\>?  
  **A:** Probably not yet, but you can submit an [issue to the github page](https://github.com/hunter-read/lfg-notify-bot/issues) or [upvote features you want to see](https://www.reddit.com/user/LFG_Notify_Bot/comments/k9heax/feature_requests/) on reddit. I have currently no features on my todo list, so please don't hesitate to ask for something.  
  
* **Q:** How can I help?  
  **A:** Best way to do so is [submit issues](https://github.com/hunter-read/lfg-notify-bot/issues) for bugs or features. And if the bot was helpful, [leave a comment on reddit with your success story or a good/bad bot message](https://www.reddit.com/user/LFG_Notify_Bot/comments/jxsf6t/accolades_and_success_stories). Or you can buy me a [coffee](https://www.buymeacoffee.com/HunterRead). 

* **Q:** You should make an app/website.  
  **A:** I like reddit and overall the lfg subreddit is full of good people, but also getting a app/website with the user base needed to sustain it is very difficult. There is [now a web page to subscribe](https://readpnw.dev/lfg) to the bot easily however.

Have a question, that is not answered here? [Send the developer a message](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Question)
  
