import os
import re
import asyncio
import discord
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands
from requests_html import HTMLSession

# used to retreieve bot token from .env file
load_dotenv()

# Create an instance of the discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def find_tweet(url):
    # initialize an HTTP session to scrape data
    session = HTMLSession()

    tweets = []
    # get html data from the url
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    
    # partial url for a twitter post from Bungie
    partial_url = 'https://twitter.com/BungieHelp/status/'
    
    # retrieve all BungieHelp tweet hyperlinks
    links = soup.findAll('a', href=re.compile(partial_url))

    for link in links:
        # find the parent div of the link
        parent_div = link.find_parent("div")
        # search for spans in order to find the tweet posting time
        spans = parent_div.find_all("span", string = re.compile("hours?|mins?"))
        for span in spans:
            time = span.text
            # filter span tags to retrieve post times of tweets
            if 'hours' in time and int(time[0]) <= 2 and time[1] == ' ' or 'min' in time:
                # if tweet was posted an hour ago or less, add url to valid tweets
                tweets.append(link['href'])
    session.close()
    return tweets
             
@bot.command(pass_context=True)
async def send_array_contents(array):
    prev_msg = []
    # channel I want to send the link to
    channel = bot.get_channel(int(os.getenv('CHANNEL_ID')))
    # check if the message has already been sent (avoids duplicates when resetting bot)
    async for message in channel.history(limit=20):
        prev_msg.append(message.content)
    dupeCount=0
    for msg in prev_msg:
        for link in array:
            if link == msg:
                print("Dupe", link)
                dupeCount+=1
                array.remove(link)
    if dupeCount > 0:            
        print("Duplicate tweet(s) found. Trying Again in 30 minutes.")

# function to find the links and send them to the discord server
async def message():
    # CHANGE GOOGLE SEARCH HERE
    links = await find_tweet('https://www.google.com/search?q=bungiehelp+twitter')
    
    if(len(links) > 0):
        print("sending ", links)
        await send_array_contents(links)
    else:
        print("No tweets found, trying again in 30 minutes.")
        
@bot.event
async def on_ready():
    print("bungiebot reporting for duty!")
    # loop the search indefinitely in 30 minute intervals
    while not bot.is_closed():
        await message()
        await asyncio.sleep(1200) 

# start the bot
bot.run(os.getenv('DISCORD_TOKEN'))

