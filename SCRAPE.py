from time import sleep as sleep
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS
from tkinter import *


##class application(Frame):
##    def __init__(self, root):
##        
##
##
##
##
##
##
##
##
##instance = application(Tk())

URL = "https://www.hltv.org"
req = Request("https://www.hltv.org/results", headers={'User-Agent':'Mozilla/6.0'})


def getTable(url):
    #REMEMBER FORFEITS ARE A THING
    req = Request(url, headers={'User-Agent':'Mozilla/6.0'})
    try:
        webpage = urlopen(req)
    except HTTPError as e:#If there is a server error
        print("e")#show the error
    except URLError as e:#If URL does not exist
        print("Server could not be found")
    else:#If there are no errors
        #Scrapes
        #                  <div class="box-headline flexbox nowrap header">
        html = BS(webpage.read(), "html.parser")
        #Find out if it is LAN and if it is best of 3
        #<div class="padding preformatted-text">Best of 3 (LAN)
        #Someones name could have a 3 or a 1 in it so i need to make sure when it says someone is standing in for someone
        #it still successfully finds out if it is best of 3 of 1, or 2 or 5
        #
        #
        #but also if the name also has LAN in it.
        text = html.find("div", {"class":"padding preformatted-text"}).getText()
        print(text)
        text = html.find("div", {"class":"event text-ellipsis"}).getText()
        print(text)
        try:
            latestResult = html.find("div", {"class": "small-padding stats-detailed-stats"}).find("a", href=True)
        except:
            ohnoes()
            #One issue could be that there is a table, but it doesnt have all the maps!
        else:
            url = "".join([URL, latestResult["href"]])
            print(url)
            print("waiting 5 seconds")
            sleep(5)

            req = Request(url, headers={'User-Agent':'Mozilla/6.0'})
            try:
                webpage = urlopen(req)
            except HTTPError as e:#If there is a server error
                print("e")#show the error
            except URLError as e:#If URL does not exist
                print("Server could not be found")
            else:#If there are no errors
                #Scrapes
                html = BS(webpage.read(), "html.parser")
                latestResult = html.findAll("table", {"class":"stats-table"})
        return(latestResult)

def lookAtTable(data):
    teamName = data.find("th", {"class":"st-teamname text-ellipsis"}).getText()
    print(teamName)
    name = data.findAll("td", {"class":"st-player"})#Finds the HTML tag containing each players name
    #data.findAll("span", {"class":"gtSmartphone-only"}).decompose
    #i need too find a way to remove this. This command doesn work.
    kills = data.findAll("td",{"class":"st-kills"} )
    deaths = data.findAll("td", {"class": "st-deaths"})
    kast = data.findAll("td", {"class":"st-kdratio"})
    adr=data.findAll("td", {"class":"st-adr"})
    #fkDiff=data.findAll("td", {"class":"st-fkdiff won", "class":"st-fkdiff lost"})
    #it either gets won or lost, i need both
    rating=data.findAll("td", {"class":"st-rating"})
    for i in range (len(name)):#Goes through every person in game
        #above is the len because if it is a best of 3 and if a standin comes for the
        #third map, it is going to have 6 players instead of 5
        print(name[i].getText())#Prints only the text f the player name
        print(kills[i].getText())
        print(deaths[i].getText())
        print(kast[i].getText())
        print(adr[i].getText())
        #print(fkDiff[i].getText())
        #doesnt work see above
        print(rating[i].getText())
        print("NEXT")
        print("")
        print("PLAYER:")
def ohnoes():
    print("oh no there is no table")
    #One issue could be that there is a table, but it doesnt have all the maps!

lastResult = ""#There is no last result so it is empty(the last result is the most recent web scraped result, so it doesnt scrape twice)
while True:
    try:
        webpage = urlopen(req)#Open hltv results page
    except HTTPError as e:#If there is a server error
        print("e")#show the error
    except URLError as e:#If URL does not exist
        print("Server could not be found")
    else:#If there are no errors
        #Scrapes
        html = BS(webpage.read(), "html.parser")#the html is stored
##        try:#If there is more than one featured results, it only removes one.
##            html.find('h1', {"class": "standard-headline inline"})#if this exists(is there featured results)
##            #messy.........
##        except:
##            print("There is no featured results")
##        else:#if there is no errors, meaning there is featured results
##            print("There is a featured results, removing!")
##            html.find('div', {"class":"results-sublist"}).decompose()#no errors means there is a featured results, so this line removes the features results.
        #above doesnt work anymore, tbh fair enough it was crap code
        latestResult = html.find("div", {"class":"result-con"}).find("a", href=True)#Finds the latest result
        aaa = "".join([URL, latestResult["href"]])#Finds the HREF link, adds it to URL
        if aaa != lastResult:
            lastResult = aaa
            print(aaa)
            print("Received URL from HTML, scraping URL in 5 seconds...")
            sleep(5)
            data = getTable(aaa)
            table1 =data[0]
            table2 = data[1]
            lookAtTable(table1)
            lookAtTable(table2)
        else:
            print("That was the old url, no need to scrape again!!!")
        print("Done, waiting 90 seconds before scraping again...")
        sleep(90)
