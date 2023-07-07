import discord
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from discord.ext import commands
import asyncio


load_dotenv()
# initialize an HTTP session
session = HTMLSession()

intents = discord.Intents.default()
intents.message_content = True

# Create an instance of the bot
bot = commands.Bot(command_prefix='!', intents=intents)

async def find_tweet(url):
    
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    
    links = set()
    divs = (soup.find_all('div', {"class":"fy7gGf"}))
    for div in divs:
        if div.find("a", {"class":"h4kbcd"}):
            #paragraphs = [p.text for p in soup.find_all('p')]
            time_tags = [d.text for d in div.find_all("span", {"class":"f"})]
            regex = re.compile('.·')
            #remove · character from time list, this is the only way I could think to remove it
            time = [i for i in time_tags if not regex.match(i)]
            #if 'hour' in time[0] and int(time[0][0]) > 1 or 'mins' in time[0]:
            if 'day' in time[0] and int(time[0][0]) >= 1 or 'mins' in time[0]:
                #times.append(time[0])
                link = div.find("a")
                links.add( link['href'] )
    #pprint(list(links))
    return links
    
@bot.command(pass_context=True)
async def send_array_contents(array):
    channel = bot.get_channel(1126904064119152771) 
  
    for item in array:
        print(item)
        #await channel.send(item)

async def message():
    links = await find_tweet('https://www.google.com/search?q=bungiehelp')
    await send_array_contents(links)
        
@bot.event
async def on_ready():
    print("bot logged in")
    while not bot.is_closed():
        await message()  # Run the Bot
        await asyncio.sleep(3600) # Wait 1 hour to check for new tweets

bot.run(os.getenv('DISCORD_TOKEN'))