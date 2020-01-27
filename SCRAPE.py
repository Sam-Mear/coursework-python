from time import sleep as sleep
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS
from datetime import date


URL = "https://www.hltv.org"
req = Request("https://www.hltv.org/results", headers={'User-Agent':'Mozilla/6.0'})


def getTable(url):
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

        #Before anything, it needs to check if the result is valid, "1" under the teams logo means match page is invalid.

        #i am looking for <div class="won">1</div>, if it exists then i know this result isnt valid to be scraped, check design segment.
        try:#I need to use try at the moment, just because there might be a rare case of tie, and the class won wont be there or correct
            classWon = html.find("div", {"class":"won"}).getText()
            if classWon == "1":
                valid = False
            else:
                valid = True
        except:
            valid = True
        if valid == False:
            print("aaaaaaaaaaaaaa i havent programmed this in properly yet, but this means the match page isnt valid, but the program will try its hardest to work :((((")




        
        #                  <div class="box-headline flexbox nowrap header">
        #Find out if it is LAN and if it is best of 3
        #<div class="padding preformatted-text">Best of 3 (LAN)
        #Someones name could have a 3 or a 1 in it so i need to make sure when it says someone is standing in for someone
        #it still successfully finds out if it is best of 3 of 1, or 2 or 5
        #
        #
        #but also if the name also has LAN in it.


        #The program still needs to do checks to make sure the matchpage is okay for webscraping
        #The next check is to make sure all the stats tables are there, if the web scraper is too
        #quick on the match page, hltv might have only had enough time for the first few maps, and
        #not the closing map.
        
        #<div class="box-headline flexbox nowrap header">
        maplist = html.find("div",{"class":"box-headline flexbox nowrap header"})
        maplist = maplist.find("div",{"class":"flexbox nowrap"})#There would normally be loads of these div with class small-padding
        maplist = maplist.findAll("div",{"class":"small-padding"})
        #but i search only html for div class box-headline flexbox nowrap header, which is specific to one bit.
        numberOfMaps = (len(maplist)-1)
        print("there is {0} number of map(s)".format(numberOfMaps))
        #Now to check how many maps there is supposed to be
        #I already have classWon from a different thing, so i only need to scrape classLost
        classLost = html.find("div", {"class":"lost"}).getText()
        mapsCheck = int(classLost)+int(classWon)
        #Checking if theyre the same
        if mapsCheck >5:
            print("dont worry about maps check, its only a best of 1")
            #remember to explain in design the reason why this check doesnt work for best of 1 and what i have put into place to check best of ones.
        elif mapsCheck == numberOfMaps:
            print("All stats are there")
        else:
            print("RESULT MISSING DATA!")
            return("MissingMap(s)")

        #Getting all map names:
        mapListNamesHTML = html.findAll("div",{"class":"mapname"})
        mapListNames = []
        for i in range(len(mapListNamesHTML)):
            mapListNames.append(mapListNamesHTML[i].getText())
        print(mapListNames)
        #Map names done
        #It doesnt matter if we take 3 maps, but two is played because it was a 2-0
        #because in lookAtTable, we can deal with this...
        text = html.find("div", {"class":"padding preformatted-text"}).getText()
        print(text)
        text = html.find("div", {"class":"event text-ellipsis"}).getText()
        print(text)#Event
        print(date.today())
        try:#rather yucky way of seeing if there is at least one stats table
            #although i need to confirm this works at some point
            latestResult = html.find("div", {"class": "small-padding stats-detailed-stats"}).find("a", href=True)
        except:
            ohnoes()
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
                if numberOfMaps == 1:#Best of 1
                    latestResult = html.findAll("table", {"class":"stats-table"})
                else:#Others
                    mapListHTML = []
                    mapListURL = []
                    mapListHTML = html.findAll("a", {"class":"col stats-match-map standard-box a-reset inactive"})
                    for i in range(len(mapListHTML)):
                        mapListURL.append(mapListHTML[i].get("href"))
                    latestResult = sUbBrROuTiNE(mapListURL)


        return(latestResult)

def sUbBrROuTiNE(mapListURL):#This subroutine only gets called when the match is not a best of 1.
    mapsTables = []
    for i in range(len(mapListURL)):
        url = "".join([URL, mapListURL[i]])
        print(url)
        print("waiting 5 seconds")
        sleep(5)
        req = Request(url, headers={'User-Agent':'Mozilla/6.0'})
        try:
            webpage = urlopen(req)#Open hltv results page
        except HTTPError as e:#If there is a server error
            print("e")#show the error
        except URLError as e:#If URL does not exist
            print("Server could not be found")
        else:#If there are no errors
            #Scrapes
            html = BS(webpage.read(), "html.parser")
            for each in html.findAll("table", {"class":"stats-table"}):
                mapsTables.append(each)
    return(mapsTables)

def lookAtTable(data):#Data imported is the tables, not the whole html page
    numberOfMaps = (len(data)//2)#Theres two sets of tables for each map.
    
    for i in range(len(data)):
        print("""

Map Number {0}

""".format(i/2))
        currentTable = data[i]
        teamName = currentTable.find("th", {"class":"st-teamname text-ellipsis"}).getText()
        print(teamName)
        name = currentTable.findAll("td", {"class":"st-player"})#Finds the HTML tag containing each players name
        #data.findAll("span", {"class":"gtSmartphone-only"}).decompose
        #i need too find a way to remove this. This command doesn work.
        kills = currentTable.findAll("td",{"class":"st-kills"} )
        deaths = currentTable.findAll("td", {"class": "st-deaths"})
        kast = currentTable.findAll("td", {"class":"st-kdratio"})
        adr=currentTable.findAll("td", {"class":"st-adr"})
        #fkDiff=data.findAll("td", {"class":"st-fkdiff won", "class":"st-fkdiff lost"})
        #it either gets won or lost, i need both
        rating=currentTable.findAll("td", {"class":"st-rating"})
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

def checkingForMap(URL):
    print("Only goes here if there is a stats table missing")
    print("Ill give it 3 tries. if it fails on all, it will give up and move on")
    count = 0
    while count <3:
        print("Waiting 30 seconds")
        sleep(30)
        data = getTable(latestResultURL)
        if data == "MissingMap(s)":
            count = count +1
        else:
            print("All stats are now there")
            lookAtTable(data)

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
        temp = html.find('div', {"class": "big-results"})#if this doesnt exists(is there featured results)
            #messy.........
        if temp == None:
            print("There is no featured results")
        else:#if there is no errors, meaning there is featured results
            print("There is a featured results, removing!")
            html.find('div', {"class":"big-results"}).decompose()#no errors means there is a featured results, so this line removes the features results.
        #above doesnt work anymore, tbh fair enough it was crap code
        #still crap but ammended it so it works...
        latestResult = html.find("div", {"class":"result-con"}).find("a", href=True)#Finds the latest result
        latestResultURL = "".join([URL, latestResult["href"]])#Finds the HREF link, adds it to URL
        missingMap = False
        if latestResultURL != lastResult:
            lastResult = latestResultURL
            print(latestResultURL)
            print("Received URL from HTML, scraping URL in 5 seconds...")
            sleep(5)
            data = getTable(latestResultURL)
            if data == "MissingMap(s)":
                missingMap = True
            else:
                lookAtTable(data)
        else:
            print("That was the old url, no need to scrape again!!!")
        if missingMap == True:
            checkingForMap(latestResultURL)
            print("Done, waiting 25 seconds before scraping again...")
            sleep(25)
        else:
            print("Done, waiting 90 seconds before scraping again...")
            sleep(90)
