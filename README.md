
<h1 align="center">
  <br>
  <a href="http://twitter.com/thenasabot"><img src="https://i.imgur.com/w8o4VH0.png" alt="TheNasaBot" width="200"></a>
  <br>
  The Nasa Images Bot
  <br>
</h1>

<h4 align="center">A Twitter bot using the <a href="https://api.nasa.gov/" target="_blank">NASA API</a></h4>

<p align="center">
  <a href="https://twitter.com/intent/tweet?text=Hey%20@TheNasaBot" target="_blank">
    <img src="https://img.shields.io/badge/Try Now-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white"
         alt="Twitter">
  </a>
</p>

<p align="center">
  <a href="#about-">About</a> •
  <a href="#how-to-use-">How To Use</a> •
  <a href="#set-up-">Set-Up</a> •
  <a href="#related-">Related</a> •
  <a href="#contact-">Contact</a>
</p>

<p align="center">
  <a href="https://twitter.com/TheNasaBot">
    <img src="https://i.imgur.com/9q5j8wd.jpg">
</a>

</p>

---
## About :
### A twitter bot that replies to requests with random images from NASA's Image Gallery fetched using NASA's Open API. It also posts daily NASA's Astronomy Picture of the Day(APOD). You can also request the bot for APOD of a specific date and it will respond accordingly.

### *Some Features:*
- Does not repeat images.
- Supports banning images
- Supports blocking specific users.
- All config done using separete settings file.
---
## How To Use :

* Tweet <a href="https://twitter.com/intent/tweet?text=Hey%20@TheNasaBot" target="_blank">"Hey @TheNasaBot"</a> for a random image pulled from NASA's Image Library
* Tweet <a href="https://twitter.com/intent/tweet?text=Hey%20@TheNasaBot%20#Mars" target="_blank">"Hey @TheNasaBot #keyword"</a> to get am image matching the keyword - eg. #Jupiter
* Tweet <a href="https://twitter.com/intent/tweet?text=Hey%20@TheNasaBot%20send%20APOD%20for%20#2020-03-15" target="_blank">"Hey @TheNasaBot send APOD for #YYYY-MM-DD"</a> to get NASA's Astronomy Picture of the Day for the specified date - eg. #2021-02-10

---

## Set Up :

- *Requirements:*
    * python3
    * tweepy `pip install tweepy`
    * requests `pip install requests`
    * <a href="https://developer.twitter.com/en/portal/petition/essential/basic-info" target="_blank">Twitter developer account</a>

- *Files setup:*
    * Rename all `sample-filename` files to `filename`
    * Complete the `settings/settings` file with appropriate details
    <br>([Detailed explaination](#settings-file-config) below)
    * Finally setup a cron job to run `twitterbot.py`
    <br> Eg. `* * * * * python3 /path/to/bot/twitterbot.py`

- *Monitoring:*
    * You can use a service like <a href="https://cronitor.io/" target="_blank">Cronitor</a> to monitor the bot and get notified in case of any errors.

### *Settings file config:*

- `twt_api_key` - Twitter consumer key
- `twt_secret_key` - Twitter consumer key secret
- `twt_token` - Twitter access key
- `twt_secret_token` - Twitter access key secret
- `nasa_api_key` - NASA API key (Get it <a href="https://api.nasa.gov/" target="_blank">here.</a>)
- `allow_repeat_after` - After how many images the bot is allowed to repeat an image
- `apod_time` - Time in HH:MM format (24 hours) when the bot should post the daily APOD
- `bot_account` - @Username of the bot account
- `master_account` - @Username of the bot manager/owner account
- `temp_downloads` - Full path to a folder where bot can download images temporarily
- `search_terms` - [list] of search terms the bot should use when looking for images. (The bot will choose a random image from the search results)
- `ban_command` - Keyword that the manager/owner can tweet under any reply from the bot. This will result in the bot deleting that reply and it will not post that image again.
- `request_commands` - Keyword/s that the users can use when requesting an image from the bot. For multiple keywords, add each on a new line.
- `time_tolerance` - Time (in minutes) for how old a request tweet should be for it to be ignored. 
- `tweet_text` - Optional text which will be added to the begining of every tweet by the bot

---

## Related :
- [twitterImgBot](https://github.com/joaquinlpereyra/twitterImgBot) - Source for twitter bot components
- [Twitter Developer Account](https://developer.twitter.com/en/portal/petition/essential/basic-info)
- [tweepy-docs](https://docs.tweepy.org/en/stable/)
- [NASA API Details](https://api.nasa.gov/#browseAPI)

---
## Contact :
<a href="https://spandanathaide.in" target="_blank">
    <img src="https://img.shields.io/badge/MY%20WEBSITE-spandanathaide.in-green?style=for-the-badge&logo=googlechrome&logoColor=white"
         alt="my website">
  </a>
<br>
<a href="https://twitter.com/SpandanAthaide" target="_blank">
    <img src="https://img.shields.io/badge/TWITTER-@SpandanAthaide-blue?style=for-the-badge&logo=twitter&logoColor=white"
         alt="Twitter">
  </a>



