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

URL = "https://www.hltv.org"
req = Request("https://www.hltv.org/results", headers={'User-Agent':'Mozilla/6.0'})

def lookAtResult(url,date):
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
        
        try:
            maplist = html.find("div",{"class":"box-headline flexbox nowrap header"})
            maplist = maplist.find("div",{"class":"flexbox nowrap"})#There would normally be loads of these div with class small-padding
            maplist = maplist.findAll("div",{"class":"small-padding"})
        except:
            print("Oh, its a best of 1 but without any tables of data...")
            return("MissingMap(s)")
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
        eventID = eventDatabaseEntry(text)
        if classWon == "2":
            gameFormat = "Best of 3"
        elif classWon == "3":
            gameFormat = "Best of 5"
        else:
            gameFormat = "Best of 1"
        gameID = gameDatabaseEntry(gameFormat, numberOfMaps, date, eventID)
        latestResult = html.find("div", {"class": "small-padding stats-detailed-stats"}).find("a", href=True)
        url = "".join([URL, latestResult["href"]])
        print(url)
        return(url,numberOfMaps,gameID,roundsWon)

def getTable(url,numberOfMaps):
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
            mapTableList = html.findAll("table", {"class":"stats-table"})
            return(True,mapTableList)
        else:#Others
            mapListHTML = []
            mapListURL = []
            mapListHTML = html.findAll("a", {"class":"col stats-match-map standard-box a-reset inactive"})
            for i in range(len(mapListHTML)):
                mapListURL.append(mapListHTML[i].get("href"))
            return(False,mapListURL)

def eventDatabaseEntry(eventName):
    cursor.execute("SELECT * FROM Event WHERE EventName = (?)",(eventName,))
    temp = cursor.fetchall()
    if temp == []:
        cursor.execute("INSERT INTO Event (EventName) VALUES (?)",(eventName,))
        cursor.execute("COMMIT")
        print("Event stored in database, getting ID")
        cursor.execute("SELECT EventID FROM Event WHERE EventName = (?)",(eventName,))
        for i in cursor.fetchall():
            return(i[0])
    else:
        print("Event is already in database, getting ID")
        for i in temp:#This is messy but it brings out the tuple from the list
            if len(i)==2:#Makes sure there is only one item in the tuple, theres no reason as to why it shouldnt, but this is keeping sure.
                return(i[0])
    
def gameDatabaseEntry(gameFormat, numberOfMaps, date, event):
    cursor.execute("INSERT INTO Game (Format,NumberOfMaps,Date,EventID) VALUES (?,?,?,?)",(gameFormat, numberOfMaps, date, event,))
    cursor.execute("COMMIT")
    return(cursor.lastrowid)

def gameMapDatabaseEntry(map, rounds, gameID):
    cursor.execute("INSERT INTO gameMap (RoundsPlayed,MapName,GameID) VALUES (?,?,?)",(rounds,map,gameID,))
    cursor.execute("COMMIT")
    return(cursor.lastrowid)

def multipleMapsHandler(mapListURL,gameID,roundsWon):#This subroutine only gets called when the match is not a best of 1.
    for i in range(len(mapListURL)):
        count = 0
        for each in roundsWon:
            if count == i:
                mapRoundsWon = {each:roundsWon[each]}
                break
            count+=1#have to have count because annoyingly, dictionaries arent ordered.
        mapsTables = []
        url = "".join([URL, mapListURL[i]])
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
            mapsTables = html.findAll("table", {"class":"stats-table"})
        lookAtTable(mapsTables,gameID,mapRoundsWon)

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

def playerDatabaseManager(playerName,nationality,teamID):# This subroutine checks if a player exists, if not the player is added, then it checks if the player's linked team is correct
    #First check is if player exists,
    #next is to check that the team hes playing for is correct.
    cursor.execute("SELECT NickName,Nationality FROM Player WHERE NickName = (?) AND Nationality = (?)",(playerName,nationality,))
    if cursor.fetchall() == []:
        #Player does not exist
        cursor.execute("INSERT INTO Player (NickName,Nationality,TeamID) VALUES(?,?,?)",(playerName,nationality,teamID))
        cursor.execute("COMMIT")
        return(cursor.lastrowid)
    #Onto second check... Only relevent to players that are already in the database.
    else:
        cursor.execute("SELECT TeamID,PlayerID FROM Player WHERE NickName = (?)",(playerName,))
        for i in cursor.fetchall():#This is messy but it brings out the tuple from the list
            if len(i)==2:#Makes sure there is only one item in the tuple, theres no reason as to why it shouldnt, but this is keeping sure.
                if i[0] == teamID:
                    print("The current teamID for this player is correct!")
                else:
                    print("Previous results show this player is in a different team")
                playerID = i[1]
            else:
                print("ERROR checking a player's TeamID... Was there more than one player named " + playerName+"?")
        return(playerID)

def teamMapDatabaseEntry(mapName,roundsWon,roundCount,teamID,gameMapID):
    roundsLost = roundCount-roundsWon
    if roundsWon > roundsLost:
        won = "w"
    elif roundsWon == roundsLost:
        won = "t"
    else:
        won = "l"
    cursor.execute("INSERT INTO TeamMap (GameMapID,TeamID,Won,RoundsWon,RoundsLost) VALUES (?,?,?,?,?)",(gameMapID,teamID,won,roundsWon,roundsLost,))
    cursor.execute("COMMIT")

def playerMapDatabaseEntry(mapID,playerID,kills,deaths,adr,kast,rating):
    cursor.execute("INSERT INTO PlayerMap (GameMapID,PlayerID,Kills,Deaths,adr,kast,Rating) VALUES (?,?,?,?,?,?,?)",(mapID,playerID,kills,deaths,adr,kast,rating,))
    cursor.execute("COMMIT")

#def lookAtTable(tableData, teamData, gameMapID):#Data imported is the tables, not the whole html page    
def lookAtTable(tableData,gameID,teamData):
    for each in teamData:
        #Theres only ever going to be one item in this... maybe it was better off afterall to make it a list 
        #instead of a dictionary.
        roundCount = 0
        print(teamData)
        for k in teamData[each]:
            roundCount += teamData[each][k]
        gameMapID = gameMapDatabaseEntry(each, roundCount, gameID)
    for tableLoopIndex in range(len(tableData)):
        print("""

Map Number {0}

""".format(tableLoopIndex/2))
        currentTable = tableData[tableLoopIndex]
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
        teamMapDatabaseEntry(each,teamData[each][teamName],roundCount,teamID,gameMapID)
        name = currentTable.findAll("td", {"class":"st-player"})#Finds the HTML tag containing each players name
        nationality = []
        for i in name:
            nationality.append((i.find("img", alt = True))['alt'])
        #<img alt="Thailand"
        #data.findAll("span", {"class":"gtSmartphone-only"}).decompose
        #i need too find a way to remove this. This command doesn work.
        kills = currentTable.findAll("td",{"class":"st-kills"} )
        deaths = currentTable.findAll("td", {"class": "st-deaths"})
        kast = currentTable.findAll("td", {"class":"st-kdratio"})
        adr=currentTable.findAll("td", {"class":"st-adr"})
        rating=currentTable.findAll("td", {"class":"st-rating"})
        for i in range (len(name)):#Goes through every person in game
            #above is the len because if a player has a technical issue, and a 6th player comes on as a standin.
            print(name[i].getText())#Prints only the text of the player name
            print(nationality[i])
            playerID = playerDatabaseManager(name[i].getText(),nationality[i],teamID)#REMEMBER TO ADD NATIONALITY TO PLAYERSSSSSS
            print(kills[i].getText())
            print(deaths[i].getText())
            print(kast[i].getText())
            print(adr[i].getText())
            print(rating[i].getText())
            playerMapDatabaseEntry(gameMapID,playerID,int(kills[i].getText().split()[0]),int(deaths[i].getText()),float(adr[i].getText()),float(kast[i].getText().split('%')[0]),float(rating[i].getText()))
            print("NEXT")
            print("")
            print("PLAYER:")

def checkingForMap(URL):
    print("Only goes here if there is a stats table missing")
    print("Ill give it 3 tries. if it fails on all, it will give up and move on")
    count = 0
    while count <3:
        print("Waiting 30 seconds")
        sleep(30)
        data = lookAtResult(URL)
        if data[0] == "MissingMap(s)":
            count = count +1
        else:
            print("All stats are now there")
            lookAtTable(data[0],data[1],data[2])


def getAllResultsOnPage(resultsPage):
    req = Request(resultsPage, headers={'User-Agent':'Mozilla/6.0'})
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
        #<div class="results-sublist"><span class="standard-headline">Results for November 16th 2019</span>
        returnedList = []
        latestResult = html.findAll("div", {"class":"results-sublist"})
        for i in range(len(latestResult)):
            dateString = latestResult[i].find("span", {"class":"standard-headline"}).getText()
            string2 = (dateString.split('for ')[1])
            string3 = string2.split(' ')
            string3[1] = string3[1].split('th')[0]
            string3[2] = string3[2].split('0')[1]
            if string3[0] == "November":
                string3[0] = "11"
            elif string3[0] == "December":
                string3[0] = "12"
            elif string3[0] == "January":
                string3[0] = "01"
            elif string3[0] == "February":
                string3[0] = "02"
            list1 = [string3[2],string3[0],string3[1]]
            print("-".join(list1))
            returnedList.append("-".join(list1))
            results = latestResult[i].findAll("div", {"class":"result-con"})
            for j in range(len(results)):
                results[j] = results[j].find("a", href=True)
                results[j] = "".join([URL, results[j]["href"]])
            returnedList.append(results)
        latestResult = html.findAll("div", {"class":"result-con"})#Finds the latest result
        return returnedList
        
        
def main():
    resultsPage = ["https://www.hltv.org/results?offset=","36"]
    lastResult = ''
    while int(resultsPage[1])>=0:
        resultURL = getAllResultsOnPage("".join(resultsPage))
        print(resultURL)
        resultURL = ['2-02-17', ['https://www.hltv.org/matches/2339143/w7m-vs-soberano-clutch-season-2', 'https://www.hltv.org/matches/2339652/skade-vs-spirit-flashpoint-europe-closed-qualifier', 'https://www.hltv.org/matches/2339643/hard-legion-vs-nemiga-oga-counter-pit-season-7', 'https://www.hltv.org/matches/2339631/unicorns-of-love-vs-japaleno-esea-mdl-season-33-europe']]
        for i in range(len(resultURL)):
            if i ==0 or (i%2)==0:
                print(resultURL[i])
                date = resultURL[i]
            else:
                for j in range(len(resultURL[i])):

                    print("waiting 10 seconds")
                    sleep(10)
                    data = lookAtResult(resultURL[i][j],date)
                    missingMap = False
                    if data == "MissingMap(s)":
                        missingMap = True
                    elif data == "False":
                        print("ignored!")
                    else:
                        print(data)
                        url = data[0]
                        numberOfMaps = data[1]
                        gameID = data[2]
                        roundsWon = data[3]
                        print("waiting 5 seconds")
                        sleep(5)
                        data = getTable(url,numberOfMaps)
                        if data[0]==True:#If it is a best of 1
                            lookAtTable(data[1],gameID,roundsWon)
                        else:#not best of 3
                            multipleMapsHandler(data[1],gameID,roundsWon)
                else:
                    print("That was the old url, no need to scrape again!!!")
        print("waiting 120 seconds...")
        sleep(120)
        resultsPage[1] = str(int(resultsPage[1]) - 100)

        
            

main()