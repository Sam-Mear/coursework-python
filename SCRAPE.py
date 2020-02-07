from time import sleep as sleep
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS
from datetime import date
import sqlite3

mydb = sqlite3.connect("CSGO-Results.db")
cursor = mydb.cursor()

#order of data entry should be 
#Team, Player, Event, Game, GameMap, PlayerMap, TeamMap
gameTableInsert = []
gameMapTableInsert = []
playerMapTableInsert = []
teamMapTableInsert = []

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

        #Before anything, it needs to check if the result is valid, "1" under the winning teams logo means match page is invalid.

        #i am looking for <div class="won">1</div>, if it exists then i know this result isnt valid to be scraped, check design segment.
        try:#I need to use try at the moment, just because there might be a(very) rare case of tie, and the class won wont be there or correct
            classWon = html.find("div", {"class":"won"}).getText()
            if classWon == "1":
                valid = False
            else:
                valid = True
        except:
            valid = True
        if valid == False:
            print("Result isnt valid... ignoring...")
            return("False")




        
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
        
        #---IMPORTANT---#
        #IF THERE IS AN ERROR BELOW THIS COMMENT, IT MEANS THERE ISNT A STATS TABLE YET
        maplist = html.find("div",{"class":"box-headline flexbox nowrap header"})
        maplist = maplist.find("div",{"class":"flexbox nowrap"})#There would normally be loads of these div with class small-padding
        maplist = maplist.findAll("div",{"class":"small-padding"})
        #but i search only html for div class box-headline flexbox nowrap header, which is specific to one bit.
        numberOfMaps = (len(maplist)-1)
        #Now to check how many maps there is supposed to be
        #I already have classWon from a different thing, so i only need to scrape classLost
        classLost = html.find("div", {"class":"lost"}).getText()
        mapsCheck = int(classLost)+int(classWon)
        print("there are {0} tables of data for {1} map(s)".format(numberOfMaps,mapsCheck))
        #Checking if theyre the same
        if mapsCheck >5:
            print("dont worry about maps check, its only a best of 1")
            mapsCheck=1
            #remember to explain in design the reason why this check doesnt work for best of 1 and what i have put into place to check best of ones.
        elif mapsCheck == numberOfMaps:
            print("All stats are there")
        else:
            print("RESULT MISSING DATA!")
            return("MissingMap(s)")
    
        #Getting all map names:
        mapInformation = html.findAll("div",{"class":"mapholder"})
        roundsWon = {}
        for i in range(mapsCheck):
            roundsWon.update({mapInformation[i].find("div",{"class":"mapname"}).getText():{str(mapInformation[i].find("div",{"class":"results-teamname text-ellipsis"}).getText()):int(mapInformation[i].find("div",{"class":"results-team-score"}).getText()),str((mapInformation[i].findAll("div",{"class":"results-teamname text-ellipsis"})[1]).getText()):int((mapInformation[i].findAll("div",{"class":"results-team-score"})[1]).getText())}})
        print(roundsWon)
        #Map names done
        text = html.find("div", {"class":"padding preformatted-text"}).getText()
        print(text)

        #gtSmartphone-only statsPlayerName
        #.split
        
        text = html.find("div", {"class":"event text-ellipsis"}).getText()
        print(text)#Event
        eventDatabaseEntry(text)
        #gameDatabaseEntry(text, str(date.today()),mapsCheck, FoRMAt)
        try:#rather yucky way of seeing if there is at least one stats table
            #---IMPORTANT---#
            #THIS DOES NOT WORK, LOOK ABOVE FOR OTHER IMPORTANT nOTE
            #although i need to confirm this works at some point -  i dont think this does in hindsight...
            #I also may move this to the top of the subroutine, as i think constant editing of this subroutine has moved its position/priority.
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

def eventDatabaseEntry(eventName):
    cursor.execute("SELECT EventID FROM Event WHERE EventName = (?)",(eventName,))
    if cursor.fetchall() == []:
        cursor.execute("INSERT INTO Event (EventName) VALUES (?)",(eventName,))
        cursor.execute("COMMIT")
        print("Event stored in database")
    else:
        print("Event is already in database.")

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

def checkIfTeamExists(teamName):
    teamID = 0
    cursor.execute("SELECT * FROM Team WHERE TeamName = (?)",(teamName,))
    temp = cursor.fetchall()
    if temp == []:
        return [False,teamID]#Team does not exist
    for i in temp:#This is messy but it brings out the tuple from the list
        if len(i)==2:#Makes sure there is only one item in the tuple, theres no reason as to why it shouldnt, but this is keeping sure.
            teamID = i[0]
        else:
            print("ERROR checking a team's TeamID... Was there more than one team named " + teamName+"? Using returning 0as teamID")
        return [True,teamID]#Team does exist.

def playerDatabaseManager(playerName,teamID):# This subroutine checks if a player exists, if not the player is added, then it checks if the player's linked team is correct
    #First check is if player exists,
    #next is to check that the team hes playing for is correct.
    cursor.execute("SELECT NickName FROM Player WHERE NickName = (?)",(playerName,))
    if cursor.fetchall() == []:
        #Player does not exist
        cursor.execute("INSERT INTO Player (NickName,TeamID) VALUES(?,?)",(playerName,teamID))
        cursor.execute("COMMIT")
    #Onto second check... Only relevent to players that are already in the database.
    else:
        cursor.execute("SELECT TeamID FROM Player WHERE NickName = (?)",(playerName,))
        for i in cursor.fetchall():#This is messy but it brings out the tuple from the list
            if len(i)==1:#Makes sure there is only one item in the tuple, theres no reason as to why it shouldnt, but this is keeping sure.
                if i[0] == teamID:
                    print("The current teamID for this player is correct!")
                else:
                    print("Previous results show this player is in a different team")
            else:
                print("ERROR checking a player's TeamID... Was there more than one player named " + playerName+"?")
                

def lookAtTable(data):#Data imported is the tables, not the whole html page    
    for i in range(len(data)):
        print("""

Map Number {0}

""".format(i/2))
        currentTable = data[i]
        teamName = currentTable.find("th", {"class":"st-teamname text-ellipsis"}).getText()
        print(teamName)
        team = checkIfTeamExists(teamName)
        teamID = team[1]
        if team[0] == True:
            print("This team is already in the database.")
        else:
            print("This team is not in the database... adding...")
            cursor.execute("INSERT INTO Team (TeamName) VALUES (?)",(teamName,))
            cursor.execute("COMMIT")
            cursor.execute("SELECT TeamID FROM Team WHERE TeamName = (?)",(teamName,))
            for i in cursor.fetchall():#This is messy but it brings out the tuple from the list
                if len(i)==1:#Makes sure there is only one item in the tuple, theres no reason as to why it shouldnt, but this is keeping sure.
                    teamID = i[0]
                else:
                    print("ERROR getting teamID... Was there more than one team named " + teamName+"?")
            print("Successfully added to database with team ID: {0}".format(teamID))
        name = currentTable.findAll("td", {"class":"st-player"})#Finds the HTML tag containing each players name
        #<img alt="Thailand"
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
            playerDatabaseManager(name[i].getText(),teamID)#REMEMBER TO ADD NATIONALITY TO PLAYERSSSSSS
            #One issue is if it is a  best of 3, it tries to add the players name 3 times :(
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
        data = getTable(latestResultURL)#I dont think <-- will work....... i think i need to parse it in...
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
            elif data == "False":
                print("ignored!")
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
