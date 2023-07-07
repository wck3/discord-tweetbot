import discord
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint


# initialize an HTTP session
session = HTMLSession()

def go_to_bungo(url):
    res = session.get(url)
    soup = soup = BeautifulSoup(res.html.html, "html.parser")
    
    
    '''links = soup.find_all("a", {"class": "h4kbcd"})
    for link in links:
        #print(link, "\n")
        res = session.get(link['href'])
        soup = BeautifulSoup(res.html.html, "html.parser")
        print(soup.find_all("a"), "\n")
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")'''

   
    divs_w_link = []
    divs = soup.find_all('div', {"class":"fy7gGf"})
    for div in divs:
        if div.find("a", {"class":"h4kbcd"}):
            #paragraphs = [p.text for p in soup.find_all('p')]
            time = [d.text for d in div.find_all("span", {"class":"f"})]
            time.sort()
            print(time, "\n")
            divs_w_link.append(div)
   
    
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
    


go_to_bungo('https://www.google.com/search?q=bungiehelp')
