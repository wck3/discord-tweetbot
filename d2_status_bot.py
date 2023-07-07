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
            
            if 'hour' in time[0] and int(time[0][0]) >= 1 and time[0][1] is ' ' or 'mins' in time[0]:
                link = div.find("a")
                links.add( link['href'] )
    return links
    
@bot.command(pass_context=True)
async def send_array_contents(array):
    # channel I want to send the link to
    channel = bot.get_channel(1126904064119152771) 
    # send each scraped link to the discord channel
    for item in array:
        print(item)
        await channel.send(item)

# wrapper function to find the links and send to the discord server
async def message():
    links = await find_tweet('https://www.google.com/search?q=bungiehelp+twitter')
    await send_array_contents(links)
        
@bot.event
async def on_ready():
    print("bot logged in")
    # loop the search indefinitely in 1 hour intervals
    while not bot.is_closed():
        await message()
        await asyncio.sleep(3600) 

# start the bot
bot.run(os.getenv('DISCORD_TOKEN'))

