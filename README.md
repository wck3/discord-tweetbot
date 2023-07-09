# Discord Tweetbot
A Discord bot that will post new tweets from an account directly into a Discord server's text channel. In my case I am using it to send tweets from @BungieHelp. This account is run by Bungie, the developer of the video game Destiny 2. Bungie posts the status of the game's servers as well as any large bugs that they address with the game. I wanted to share this information with my friends in an easy and automated way.
## How it Works
The bot is written in Python. Using the requests_html library the bot navigates to a google search for the BungieHelp twitter. Once at this site, it uses the Beautiful Soup library to scrape the html for any hyperlinks to a tweet from @BungieHelp. It then searches for the post time located in the 3 cards that are displayed at the top of the google search, as shown below:
<img width="600" alt="Screenshot 2023-07-08 at 9 38 16 PM" src="https://github.com/wck3/discord-tweetbot/assets/98120794/9e8f87c0-86a2-4201-ab17-bf9563fcf530">

If the time since posting is under 2 hours, the bot saves the links in a list. This list is compared with past messages in the destination text channel in the Discord server. If the url has not been send to the server in the past, the bot will post the url in the channel. This process occurs every 30 minutes, and the bot is designed to run 24/7.

### Why I did it this way
This seems unreliable, and that's because it is! If google changes how they display tweets, this bot will become useless. My original goal was to use the Twitter API to fetch the new tweets which would have made the process much simpler. However, the free tier no longer allows for reading other users tweets. Since I cannot afford the $100 dollar a month subscription to the API, I had no choice but to scrape the urls. I almost gave up on the project after discovering this, but I knew there had to be a way, no matter how janky!

## Requirements
- Python 3.11
- Discord.py==2.3.1
- bs4==0.0.1 (Beautiful Soup)
- python-dotenv==0.20.0

## How to Use

1. You must [create a discord bot](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/)
2. Create a .env file in the same directory as the python script. You must copy the bot token into the file in the format\
   DISCORD_TOKEN = 'YOUR-TOKEN-HERE'
3. Run the Python script and enjoy!

**NOTE:** If you change the Google search URL to a different Twitter account, make sure the search leads to a search that has the 3 tweet cards shown in the screenshot above

## Screenshot
<img width="400" alt="Screenshot 2023-07-08 at 9 48 00 PM" src="https://github.com/wck3/discord-tweetbot/assets/98120794/515095bb-2a05-47fb-9859-57bf9eba41c0">
