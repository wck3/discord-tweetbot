import discord
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from discord.ext import commands
import asyncio

# used to retreieve bot token from .env file
load_dotenv()

# initialize an HTTP session to scrape data
session = HTMLSession()

# Create an instance of the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



async def find_tweet(url):
    #get html data from the url
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    
    links = set()
    # scrape divs with same class as the twitter links
    divs = (soup.find_all('div', {"class":"fy7gGf"}))
    for div in divs:
        # isolate divs with the twitter links in them
        if div.find("a", {"class":"h4kbcd"}):
            # retrieve the time posted from the divs
            time_tags = [d.text for d in div.find_all("span", {"class":"f"})]
            #remove · character from the time list (it shares the same class as the time)
            regex = re.compile('.·')
            time = [i for i in time_tags if not regex.match(i)]
            # only save the tweet link if the tweet is less than an hour old
    
            if 'hour' in time[0] and int(time[0][0]) == 1 and time[0][1] == ' ' or 'mins' in time[0]:
                link = div.find("a")
                links.add( link['href'] )
    return links
    
@bot.command(pass_context=True)
async def send_array_contents(array):
    # channel I want to send the link to
    channel = bot.get_channel(1126904064119152771) 
    # send each scraped link to the discord channel
    # check if the message has already been sent (avoids duplicates when resetting bot)
    async for message in channel.history(limit=1):
        prev_link = message.content
    for link in array:
        if link != prev_link:
            print(link)
            await channel.send(link)
        else:
            print("Duplicate link. Trying Again in 30 minutes.")

# wrapper function to find the links and send to the discord server
async def message():
    links = await find_tweet('https://www.google.com/search?q=bungiehelp+twitter')
    if(len(links) > 0):
        await send_array_contents(links)
    else:
        print("No links found, trying again in 30 minutes.")
        
@bot.event
async def on_ready():
    print("bot logged in")
    # loop the search indefinitely in 30 minute intervals
    while not bot.is_closed():
        await message()
        await asyncio.sleep(1200) 

# start the bot
bot.run(os.getenv('DISCORD_TOKEN'))

