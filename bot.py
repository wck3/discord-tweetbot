import discord
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
import re
import schedule
import time


# initialize an HTTP session
session = HTMLSession()

def go_to_bungo(url):
    res = session.get(url)
    soup = soup = BeautifulSoup(res.html.html, "html.parser")
    
    links = []
    times = []
    divs = soup.find_all('div', {"class":"fy7gGf"})
    for div in divs:
        if div.find("a", {"class":"h4kbcd"}):
            #paragraphs = [p.text for p in soup.find_all('p')]
            time_tags = [d.text for d in div.find_all("span", {"class":"f"})]
            regex = re.compile('.·')
            #remove · character from time list, this is the only way I could think to remove it
            time = [i for i in time_tags if not regex.match(i)]
            #print(clean_time)
            #print(clean_time[0][0])
            print(time[0])
            if 'hours' in time[0] and int(time[0][0]) > 1 or 'mins' in time[0]:
                #times.append(time[0])
                link = div.find("a")
                links.append( link['href'] )
            
    
    #times = list(set(times))
    links = list(set(links))

    #pprint(times)
    #pprint(links)
    
    #pprint(res)

    #for div in divs_w_link:
    #    time = div.find_all("span", {"class":"f"})
    #    print(time)
    #print(divs_w_link)
    #print("Link Text:", link_text)
    #print("Href Attribute:", href)
    '''client = discord.client()
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))'''
    

# Schedule the function call every hour
schedule.every().hour.do( go_to_bungo('https://www.google.com/search?q=bungiehelp') )

# Run the scheduled task indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)



    '''links = soup.find_all("a", {"class": "h4kbcd"})
    for link in links:
        #print(link, "\n")
        res = session.get(link['href'])
        soup = BeautifulSoup(res.html.html, "html.parser")
        print(soup.find_all("a"), "\n")
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")'''


