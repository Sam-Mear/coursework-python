from tkinter import *
from tkinter import messagebox
import sqlite3,turtle
from datetime import date, timedelta, datetime
import updatePlayerTeams as UPT
from math import sqrt
import time
mydb = sqlite3.connect("CSGO-Results.db")
cursor = mydb.cursor()

class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)# Use the constructor
        #OR super().__init__(master)
        self.master = master

        self.master.title("CS Stats")
        self.date90 = date.today() - timedelta(90)
        self.date60 = date.today() - timedelta(60)
        self.date30 = date.today() - timedelta(30)
        self.grid(row=0,column=0)
        
    def mainMenu(self):
        self.mainMenuFrame = Frame(self.master)
        self.mainMenuFrame.grid()
        self.mainMenuButtonsFrame = Frame(self.mainMenuFrame)
        self.mainMenuButtonsFrame.grid(row=0,column=0,sticky="n")
        self.eventMvpPicker = Button(self.mainMenuButtonsFrame, text = "Event MVP Picker", relief = GROOVE, command = self.eventMVPPicker)
        self.eventMvpPicker.grid(row=0,column=0,pady=5)
        self.eventMvpPredictor = Button(self.mainMenuButtonsFrame, text="Event MVP Predictor", relief = GROOVE, command = self.eventMVPPredictor)
        self.eventMvpPredictor.grid(row=1,column=0, pady=5)
        self.playersOnRise = Button(self.mainMenuButtonsFrame, text = "Players on the Rise", relief = GROOVE, command = lambda: self.players("R"))
        self.playersOnRise.grid(row=2,column=0,pady= 5)
        self.playersOnTheDecline = Button(self.mainMenuButtonsFrame, text = "Players on the Decline", relief = GROOVE, command = lambda: self.players("D"))
        self.playersOnTheDecline.grid(row=3,column=0,pady= 5)
        self.teamsOnRise = Button(self.mainMenuButtonsFrame, text = "Teams on the Rise", relief = GROOVE, command = lambda: self.teams("W"))
        self.teamsOnRise.grid(row=4,column=0,pady= 5)
        self.teamsOnTheDecline = Button(self.mainMenuButtonsFrame, text = "Teams on the Decline", relief = GROOVE, command = lambda: self.teams("L"))
        self.teamsOnTheDecline.grid(row=5,column=0,pady= 5)
        self.updatePlayerTeamsButton = Button(self.mainMenuButtonsFrame, text = "Update player's teams", relief = GROOVE, command = self.updatePlayerTeams)
        self.updatePlayerTeamsButton.grid(row=6,column=0,pady= 5)
        self.manualResultEntry = Button(self.mainMenuFrame,text="Manual Result Entry", relief = GROOVE)
        self.manualResultEntry.grid(row=1,column=0,sticky="s")
        self.mainMenuOtherFrame = Frame(self.mainMenuFrame)
        self.mainMenuOtherFrame.grid(row=0,column=1,rowspan=2)
        self.line = Label(self.mainMenuOtherFrame, text = "LINE")
        self.line.grid(row=0,column=0)
        self.lab1 = Label(self.mainMenuOtherFrame, text = "Performing players")
        cursor.execute("SELECT subqry.PlayerID, round(subqry.AVERAGERATING,2), subqry.MAPCOUNT FROM (SELECT PlayerID, avg(Rating) AVERAGERATING,COUNT(Rating) MAPCOUNT FROM PlayerMap, GameMap,Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) GROUP BY PlayerID)AS subqry WHERE subqry.AVERAGERATING>1.3 AND subqry.MAPCOUNT > 10",(str(self.date90),))
        self.qry1 = cursor.fetchall()
        cursor.execute("SELECT subqry.PlayerID, round(subqry.AVERAGERATING,2), subqry.MAPCOUNT FROM (SELECT PlayerID, avg(Rating) AVERAGERATING,COUNT(Rating) MAPCOUNT FROM PlayerMap, GameMap,Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) GROUP BY PlayerID)AS subqry WHERE subqry.AVERAGERATING<0.75 AND subqry.MAPCOUNT > 10",(str(self.date90),))
        self.qry2 = cursor.fetchall()
        self.lab1.grid(row=0,column=2)
        self.improvPlayersL = Listbox(self.mainMenuOtherFrame,height = (len(self.qry1)+1))
        self.improvPlayersL.grid(row=1,column=1)
        self.improvPlayersL.insert(1, "Player Name")
        self.improvPlayersM = Listbox(self.mainMenuOtherFrame,height = (len(self.qry1)+1))
        self.improvPlayersM.grid(row=1, column=2)
        self.improvPlayersM.insert(1, "Num Maps")
        self.improvPlayersR = Listbox(self.mainMenuOtherFrame,height = (len(self.qry1)+1))
        self.improvPlayersR.grid(row=1, column=3)
        self.improvPlayersR.insert(1, "Rating")
        for i in range (len(self.qry1)):
            cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(int(self.qry1[i][0]),))
            self.improvPlayersL.insert(i+2, str(cursor.fetchall()[0][0]))
            self.improvPlayersM.insert(i+2, str(self.qry1[i][2]))
            self.improvPlayersR.insert(i+2,str(self.qry1[i][1]))
        self.lab2 = Label(self.mainMenuOtherFrame, text = "Underperforming players")
        self.lab2.grid(row=2,column=2)
        self.underPlayersL = Listbox(self.mainMenuOtherFrame,height = (len(self.qry2)+1))
        self.underPlayersL.grid(row=3,column=1)
        self.underPlayersL.insert(1, "Player Name")
        self.underPlayersM = Listbox(self.mainMenuOtherFrame,height = (len(self.qry2)+1))
        self.underPlayersM.grid(row=3, column=2)
        self.underPlayersM.insert(1, "Num Maps")
        self.underPlayersR = Listbox(self.mainMenuOtherFrame,height = (len(self.qry2)+1))
        self.underPlayersR.grid(row=3, column=3)
        self.underPlayersR.insert(1, "Rating")
        for i in range (len(self.qry2)):
            cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(int(self.qry2[i][0]),))
            self.underPlayersL.insert(i+2, str(cursor.fetchall()[0][0]))
            self.underPlayersM.insert(i+2, str(self.qry2[i][2]))
            self.underPlayersR.insert(i+2,str(self.qry2[i][1]))
        self.selectPlayerButton = Button(self.mainMenuOtherFrame,text="Select Player", relief = GROOVE, command = self.testtt)
        self.selectPlayerButton.grid(row=4,column=2)

#listbox

    def eventMVPPredictor(self):
        self.selectedTeamsList = []
        self.mainMenuFrame.destroy()
        self.eventMVPPredictorFrame = Frame(self.master)
        self.eventMVPPredictorFrame.grid()
        self.title = Label(self.eventMVPPredictorFrame, text="Event MVP Predictor")
        self.title.grid(row=0,column=0)
        self.title.config(font=("Helvetica",11))
        self.instructions = Label(self.eventMVPPredictorFrame, text = "1) Select the teams participating\n2)Press the predict button")
        self.instructions.grid(row=0,column=1, columnspan=2)
        self.teamNameEntryLabel = Label(self.eventMVPPredictorFrame, text="Team Search:")
        self.teamNameEntryLabel.grid(row=1,column=1, sticky="e")
        self.teamNameEntry = Entry(self.eventMVPPredictorFrame)
        self.teamNameEntry.grid(row=1,column=2,sticky = "w")
        self.teamNameEntry.focus()
        self.teamNameSubmit = Button(self.eventMVPPredictorFrame, text="Search", command=self.updateTeamSearch)
        self.teamNameSubmit.grid(row=1,column=3,sticky="w")
        self.selectedTeamsLabel = Label(self.eventMVPPredictorFrame, text="Selected Teams:")
        self.selectedTeamsLabel.grid(row=2,column=0)
        self.selectedTeams = Listbox(self.eventMVPPredictorFrame)
        self.selectedTeams.grid(row=3,column=0)
        self.searchResultsLabel = Label(self.eventMVPPredictorFrame,text="Team name search results:")
        self.searchResultsLabel.grid(row=2,column=1,columnspan=2)
        self.searchResults = Listbox(self.eventMVPPredictorFrame)
        self.searchResults.grid(row=3,column=1,columnspan=2)
        self.eventPredictSubFrame = Frame(self.eventMVPPredictorFrame)
        self.eventPredictSubFrame.grid(row=3,column=3)
        self.addSelectedTeamButton = Button(self.eventPredictSubFrame, text="Add selected Team", command=self.predicAddTeam)
        self.addSelectedTeamButton.grid(row=0,column=0,pady= 5)
        self.removeSelectedTeamButton = Button(self.eventPredictSubFrame, text="Remove Selected Team", command=self.predicRemTeam)
        self.removeSelectedTeamButton.grid(row=1,column=0,pady= 5)
        self.predictButton = Button(self.eventPredictSubFrame, text="Predict!", command=self.predict)
        self.predictButton.grid(row=3,column=0,pady= 5)
        self.mainMenuButton = Button(self.eventPredictSubFrame, text="Main Menu", command=self.eventPredictToMain)
        self.mainMenuButton.grid(row=4,column=0,pady=5)
    
    def predict(self):
        if len(self.selectedTeamsList)>1:
            for each in self.selectedTeamsList:
                pass
        else:
            messagebox.showerror("No Teams","Cannot predict if there are no teams selected, or if there is only one team selected")

    def predicRemTeam(self):
        if len(self.selectedTeams.curselection()) > 0:
            self.selectedTeamsList.pop(self.selectedTeams.curselection()[0])
            self.selectedTeams.delete(0,END)
            for each in self.selectedTeamsList:
                self.selectedTeams.insert(END, each[1])
        else:
            messagebox.showerror("Nothing selected","You must have something selected when removing a selected team")
    
    def predicAddTeam(self):
        if len(self.searchResults.curselection()) > 0:
            if self.recentTeamResult[self.searchResults.curselection()[0]] in self.selectedTeamsList:
                messagebox.showerror("Team Already Exists","The team you have tried to add to the selected, has already been selected")
            else:
                self.selectedTeamsList.append(self.recentTeamResult[self.searchResults.curselection()[0]])
                self.selectedTeams.insert(END,self.selectedTeamsList[len(self.selectedTeamsList)-1][1])
        else:
            messagebox.showerror("Nothing selected","You must have something selected when adding a selected team")
    
    def updateTeamSearch(self):
        if self.teamNameEntry.get() == "":
            messagebox.showerror("Nothing entered","You must have something entered when searching for teams")
        else:
            cursor.execute("SELECT * FROM Team WHERE TeamName LIKE (?)",("%"+str(self.teamNameEntry.get())+"%",))
            self.recentTeamResult = cursor.fetchall()
            self.searchResults.delete(0,END)
            for i in self.recentTeamResult:
                self.searchResults.insert(END,i[1])

    def eventPredictToMain(self):
        self.eventMVPPredictorFrame.destroy()
        self.mainMenu()
    
    def updatePlayerTeams(self):
        self.mainMenuFrame.destroy()
        self.updatePlayerTeamsFrame = Frame(self.master)
        self.updatePlayerTeamsFrame.grid()
        self.title = Label(self.updatePlayerTeamsFrame, text="Update Player's Teams")
        self.title.grid(row=0,column=0,columnspan=2)
        self.title.config(font=("Helvetica",11))
        self.autoButton = Button(self.updatePlayerTeamsFrame, text="Automatic", relief = GROOVE, command=self.updatePlayerTeamsManager)
        self.autoButton.grid(row=1,column=0)
        self.manual = Button(self.updatePlayerTeamsFrame, text="Manual", relief = GROOVE)
        self.manual.grid(row=1,column=1)
        self.mainMenuButton = Button(self.updatePlayerTeamsFrame, text="Main Menu", relief = GROOVE, command=self.playerTeamsToMainMenu)
        self.mainMenuButton.grid(row=2,column=0,columnspan=2)
    
    def updatePlayerTeamsManager(self):
        UPT.update(self.date90)
        messagebox.showinfo("Done","The team ID for each player has been automatically updated.")
    
    def playerTeamsToMainMenu(self):
        self.updatePlayerTeamsFrame.destroy()
        self.mainMenu()
    
    def players(self, riseOrDecline):
        self.mainMenuFrame.destroy()
        self.playersFrame = Frame(self.master)
        self.playersFrame.grid()
        if riseOrDecline == "R":
            cursor.execute("SELECT NSPlayerID,  Player.Nickname, (STRating - TNRating) ratingDifference FROM (SELECT NSPlayerID, (NSRating - STRating), NSRating, STRating FROM (SELECT PlayerID NSPlayerID, avg(Rating) NSRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),(SELECT PlayerID STPlayerID, avg(Rating) STRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID) WHERE NSPlayerID = STPlayerID AND (NSRating - STRating) < -0.15),(SELECT PlayerID TNPlayerID, avg(Rating) TNRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),Player WHERE NSPlayerID = TNPlayerID AND ratingDifference < -0.15 AND NSPlayerID = Player.PlayerID ORDER BY ratingDifference ASC LIMIT 10",(self.date90,self.date60,self.date60,self.date30,self.date30,date.today()))
            self.title = Label(self.playersFrame, text="Players on the Rise")
        else:
            cursor.execute("SELECT NSPlayerID,  Player.Nickname, (STRating - TNRating) ratingDifference FROM (SELECT NSPlayerID, (NSRating - STRating), NSRating, STRating FROM (SELECT PlayerID NSPlayerID, avg(Rating) NSRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),(SELECT PlayerID STPlayerID, avg(Rating) STRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID) WHERE NSPlayerID = STPlayerID AND (NSRating - STRating) > 0.15),(SELECT PlayerID TNPlayerID, avg(Rating) TNRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),Player WHERE NSPlayerID = TNPlayerID AND ratingDifference > 0.15 AND NSPlayerID = Player.PlayerID ORDER BY ratingDifference DESC LIMIT 10",(self.date90,self.date60,self.date60,self.date30,self.date30,date.today()))
            self.title = Label(self.playersFrame, text="Players on the Decline")
        self.playerQry = cursor.fetchall()
        self.title.grid(row=0,column=0)
        self.title.config(font=("Helvetica",11))
        self.playersListBox = Listbox(self.playersFrame,height = len(self.playerQry))
        self.playersListBox.grid(row=1,column=0,columnspan=2)
        self.graphButton = Button(self.playersFrame,text="Show on graph", relief = GROOVE, command=self.playersToGraph)
        self.graphButton.grid(row=0,column=1,sticky="e")
        for i in range(len(self.playerQry)):
            self.playersListBox.insert(i+1,self.playerQry[i][1])

    def playersToGraph(self):
        if len(self.playersListBox.curselection())>0:
            print(self.playersListBox.curselection())
            self.playerID = self.playerQry[self.playersListBox.curselection()[0]][0]
            self.playersFrame.destroy()
            self.graph(self.playerID)
        else:
            print("YOU DIDNT SELCTR ANYTHINC UTNT")

    def teams(self,winOrLoss):
        if winOrLoss == "W":
            cursor.execute("SELECT Team.TeamName, (CountWon-CountLost), (CountWon+CountLost) TotalMaps FROM (SELECT TeamID TeamIDWon, count(Won) CountWon FROM TeamMap,GameMap,Game WHERE TeamMap.GameMapID=GameMap.GameMapID AND GameMap.GameID=Game.GameID AND Game.Date > (?) AND TeamMap.Won = 'w' GROUP BY TeamID),(SELECT TeamID TeamIDLost, count(Won) CountLost FROM TeamMap,GameMap,Game WHERE TeamMap.GameMapID=GameMap.GameMapID AND GameMap.GameID=Game.GameID AND Game.Date > (?) AND TeamMap.Won = 'l' GROUP BY TeamID),Team WHERE TeamIDWon = TeamIDLost AND TotalMaps>15 AND TeamIDWon = Team.TeamID ORDER BY (CountWon - CountLost) DESC LIMIT 10",(self.date90,self.date90))
        else:
            cursor.execute("SELECT Team.TeamName, (CountWon-CountLost), (CountWon+CountLost) TotalMaps FROM (SELECT TeamID TeamIDWon, count(Won) CountWon FROM TeamMap,GameMap,Game WHERE TeamMap.GameMapID=GameMap.GameMapID AND GameMap.GameID=Game.GameID AND Game.Date > (?) AND TeamMap.Won = 'w' GROUP BY TeamID),(SELECT TeamID TeamIDLost, count(Won) CountLost FROM TeamMap,GameMap,Game WHERE TeamMap.GameMapID=GameMap.GameMapID AND GameMap.GameID=Game.GameID AND Game.Date > (?) AND TeamMap.Won = 'l' GROUP BY TeamID),Team WHERE TeamIDWon = TeamIDLost AND TotalMaps>15 AND TeamIDWon = Team.TeamID ORDER BY (CountWon - CountLost) ASC LIMIT 10",(self.date90,self.date90))
        self.teamsWLResult = cursor.fetchall()
        self.mainMenuFrame.destroy()
        self.teamsFrame = Frame(self.master)
        self.teamsFrame.grid()
        if winOrLoss == "W":
            self.title = Label(self.teamsFrame, text="Teams on the Rise")
        else:
            self.title = Label(self.teamsFrame, text="Teams on the Decline")
        self.title.grid(row=0,column=0,sticky="w")
        self.title.config(font=("Helvetica",11))
        self.teamsWLResultListBox = Listbox(self.teamsFrame,height = 10)
        self.teamsWLResultListBox.grid(row=1,column=0,columnspan=2)
        self.backButton = Button(self.teamsFrame,text="Back to Main Menu", relief = GROOVE, command=self.teamsToMainMenu)
        self.backButton.grid(row=0,column=1,sticky="e")
        for i in range(len(self.teamsWLResult)):
            self.teamsWLResultListBox.insert(i+1,str(self.teamsWLResult[i]))

    def teamsToMainMenu(self):
        self.teamsFrame.destroy()
        self.mainMenu()

    def eventMVPPicker(self):
        self.mainMenuFrame.destroy()
        self.eventMVPPickerFrame = Frame(self.master)
        self.eventMVPPickerFrame.grid()
        cursor.execute("SELECT EventName, Event.EventID FROM Event, Game WHERE Date > (?) AND  Game.EventID = Event.EventID GROUP BY EventName",(date.today() - timedelta(20),))
        self.eventNamesQRY = cursor.fetchall()
        self.eventNames = Listbox(self.eventMVPPickerFrame,height = (len(self.eventNamesQRY)+1),width = 70)
        self.eventNames.grid(row=0,column=0)
        self.eventNames.insert(1, "EventName,EventID")
        for i in range(len(self.eventNamesQRY)):
            self.eventNames.insert(i+2,str(self.eventNamesQRY[i]))
        self.buttonSelectEvent = Button(self.eventMVPPickerFrame,text="Select Event", relief = GROOVE,command = self.EventSelection)
        self.buttonSelectEvent.grid(row=0,column=1)

    def EventSelection(self):
        if len(self.eventNames.curselection())>0 and self.eventNames.curselection() != 0:
            eventID = self.eventNamesQRY[self.eventNames.curselection()[0]-1][1]
            eventName = self.eventNamesQRY[self.eventNames.curselection()[0]-1][0]
            self.eventMVPPickerFrame.destroy()
            cursor.execute("SELECT round(AVERAGERATING,2),SUBQRYPLAYER FROM (SELECT avg(Rating) AVERAGERATING, PlayerID SUBQRYPLAYER FROM Event, Game, GameMap, PlayerMap WHERE Event.EventID = (?) AND Event.EventID = Game.EventID AND GameMap.GameID = Game.GameID AND PlayerMap.GameMapID = GameMap.GameMapID GROUP BY PlayerID ORDER BY avg(Rating) DESC LIMIT 5)",(eventID,))
            self.top5 = cursor.fetchall()
            self.eventSelectionFrame = Frame(self.master)
            self.eventSelectionFrame.grid()
            print(self.top5)
            self.title = Label(self.eventSelectionFrame, text="Event: {0}".format(eventName),borderwidth=2, relief="groove")
            self.title.grid(row=0,column=0,columnspan=3)
            self.title.config(font=("Helvetica",11))
            self.top5Players = Listbox(self.eventSelectionFrame, height=5,width=35)
            self.top5Players.grid(row=1,column = 2,rowspan=4)
            self.temp = []
            for i in range(len(self.top5)):
                cursor.execute("SELECT Nickname, TeamName FROM Player,Team WHERE PlayerID = (?) AND Player.TeamID = Team.TeamID",(self.top5[i][1],))
                self.temp.append(cursor.fetchall())
                self.temp[i].append(self.top5[i][0])
                self.top5Players.insert(i+1,str(self.temp[i]))
            self.eventStartLabel = Label(self.eventSelectionFrame, text="Event Start Date:")
            self.eventStartLabel.grid(row=1,column=0,sticky=E)
            self.eventEndLabel = Label(self.eventSelectionFrame, text="Event End Date:")
            self.eventEndLabel.grid(row=2,column=0,sticky=E)
            cursor.execute("SELECT min(Date),max(Date) FROM Game WHERE EventID = (?)",(eventID,))
            eventDates = cursor.fetchall()
            self.eventStart = Label(self.eventSelectionFrame, text=eventDates[0][0])
            self.eventStart.grid(row=1,column=1,sticky=W)
            self.eventEnd = Label(self.eventSelectionFrame, text=eventDates[0][1])
            self.eventEnd.grid(row=2,column=1,sticky=W)
            self.backToMainMenu = Button(self.eventSelectionFrame, text="Main Menu", relief = GROOVE,command=self.eventMVPPickerToMenu)
            self.backToMainMenu.grid(row=3,column=0,columnspan=2)
        else:
            print("YOU DIDNT SELECT ANYTHING CUNT")

    def eventMVPPickerToMenu(self):
        self.eventSelectionFrame.destroy()
        self.mainMenu()
    
    def testtt(self):
        print(self.improvPlayersL.curselection())
        if len(self.improvPlayersL.curselection()) > 0 and self.improvPlayersL.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersL.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        elif len(self.improvPlayersM.curselection()) > 0 and self.improvPlayersM.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersM.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        elif len(self.improvPlayersR.curselection()) > 0 and self.improvPlayersR.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersR.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        #underperforimg players
        elif len(self.underPlayersL.curselection()) > 0 and self.underPlayersL.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersL.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        elif len(self.underPlayersM.curselection()) > 0 and self.underPlayersM.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersM.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        elif len(self.underPlayersR.curselection()) > 0 and self.underPlayersR.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersR.curselection()[0]-1][0])
            self.mainMenuFrame.destroy()
            self.graph(playerID)
        else:
            print("YOU HAVENT SELECTED ANYHTING BITHC.")
        

    def graph(self,playerID):
        print(playerID)
        cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(playerID,))
        playerName = cursor.fetchall()[0][0]
        cursor.execute("SELECT Game.Date, Rating FROM PlayerMap, GameMap, Game WHERE PlayerID = (?) AND PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) ORDER BY Date DESC",(playerID,str(self.date90)))
        playerRatings = cursor.fetchall()
        average =0.0
        playerRatingsDate = []
        self.coords = []
        for i in range(len(playerRatings)):
            average += float(playerRatings[i][1])
            playerRatingsDate.append((int(str(datetime.strptime(playerRatings[i][0],'%Y-%m-%d').date()- self.date90).split(" day")[0])-45)*8)
        count = 1
        count2 = 1
        futurecharacter = ''
        outputstring = []
        for each in playerRatingsDate:
            try:
                futurecharacter = playerRatingsDate[count2]
            except:
                outputstring.append(str(count))
                break
            if each == futurecharacter:
                count +=1
            else:
                outputstring.append(str(count))
                count = 1
            count2 += 1
        temp = 0
        for i in range(len(outputstring)):
            templist = playerRatings[temp:temp+int(outputstring[i])]
            tempnumber = 0.0
            for j in range(len(templist)):
                tempnumber += float(templist[j][1])
            self.coords.append([playerRatingsDate[temp],((tempnumber/len(templist))-1)*300])
            temp += int(outputstring[i])
        average = average/len(playerRatings)
        print(average)
        avgcoords = [[-400,(average-1)*300],[400,(average-1)*300]]
        
        ##### setup #######
        h,w=600,720
        self.canvas=Canvas(master=root,height=h,width=w)
        pen=turtle.RawTurtle(self.canvas)
        pen2=turtle.RawTurtle(self.canvas)
        self.pen3=turtle.RawTurtle(self.canvas)
        pen.hideturtle()
        pen2.hideturtle()
        self.pen3.hideturtle()
        pen.speed(0)
        pen2.speed(0)
        self.pen3.speed(0)
        pen._tracer(0,0)
        pen2._tracer(0,0)
        self.pen3._tracer(1,0)
        pen2.color("blue")
        self.pen3.color("red")
        ####  axes   ############
        pen.penup()
        pen.goto(-w//2,0)
        pen.pendown()
        pen.goto(w//2,0)
        pen.penup()
        pen.goto(-1,-h//2)
        pen.pendown()
        pen.goto(-1,h//2)
        pen.penup()
        ########## axis labels ###########
        pen.goto(-w//2+30,-20)
        pen.write("-"+str(w//2)+",0")
        pen.goto(w//2-30,-20)
        pen.write(str(w//2)+",0")
        pen.goto(20,-h//2+30)
        pen.write("0,-"+str(h//2))
        pen.goto(20,h//2-30)
        pen.write("0,"+str(h//2))
        ########  self.coords  #################
        pen2.penup()
        for i in self.coords:
            pen2.goto(i)
            pen2.pendown()
            pen2.penup()
            pen2.fd(5)
            pen2.left(90)
            pen2.pendown()
            for j in range(60):
                pen2.fd(0.5)
                pen2.left(6)
            pen2.right(90)
            pen2.penup()
            pen2.back(5)
            pen2.pendown()
        self.pen3.penup()
        for i in avgcoords:
            self.pen3.goto(i)
            self.pen3.pendown()
        self.canvas.grid(row=0,column=1)

        ###### UI Around Graph ############################
        self.buttons = Frame(self.master)
        self.buttons.grid(row=0,column=0,sticky="NW")
        self.title = Label(self.buttons,text="Graph for PlayerID {0} named: {1}".format(playerID,playerName))
        self.title.grid(row=0,column=0,columnspan=2)
        self.averageLabel = Label(self.buttons,text="Average:")
        self.averageLabel.grid(row=2,column=0,sticky="E")
        self.average = Label(self.buttons,text=round(average,2))
        self.average.grid(row=2,column=1,sticky="W")
        self.newPlayerButton = Button(self.buttons, text="Graph on different player?", relief = GROOVE,command=self.playerNameChecker)
        self.newPlayerButton.grid(row=3,column=0,columnspan=2)
        self.linRegBut = Button(self.buttons, text="Perform linear regression", command= self.linRegSubrt)
        self.linRegBut.grid(row=4,column=0,columnspan=2)
        self.backButton = Button(self.buttons, text = "Main Menu", relief = GROOVE, command=self.graphToMainMenu)
        self.backButton.grid(row=5,column=0,columnspan=2)
    
    def linRegSubrt(self):
        n=len(self.coords)
        sumX = 0
        sumY = 0
        sumXSquared = 0
        sumYSquared = 0
        sumXY = 0
        for i in range(n):
            sumX += self.coords[i][0]
            sumY += self.coords[i][1]
            sumXSquared += self.coords[i][0]**2
            sumYSquared += self.coords[i][1]**2
            sumXY += self.coords[i][0]*self.coords[i][1]
        #bx+a
        sxy = sumXY-((sumX*sumY)/n)
        sxx = sumXSquared-(sumX**2/n)
        syy = sumYSquared-(sumY**2/n)
        b = sxy/sxx#works fine
        a=(sumY/n) - ((sumX/n)*b)#somethings wrong here
        self.pen3.penup()
        self.pen3.color("green")
        self.pen3.goto(-360,a+b*-360)
        self.pen3.pendown()
        print([360,a+b*-360])
        self.pen3.goto(360,a+b*360)
        self.pearsonsLabel = Label(self.buttons, text="PMCC:")
        self.pearsonsLabel.grid(row=6,column=0,columnspan=2)
        self.pearsons = Label(self.buttons, text = str(sxy/sqrt(sxx*syy)))
        self.pearsons.grid(row=7,column=0, columnspan=2)
    
    def playerNameChecker(self):
        self.buttons.destroy()
        self.canvas.destroy()
        self.playerSelector = Frame(self.master)
        self.playerSelector.grid()
        self.playerNicknameLabel = Label(self.playerSelector,text="Player Nickname:")
        self.playerNicknameEntry = Entry(self.playerSelector)
        self.playerNicknameLabel.grid(row=0,column=0,sticky="e")
        self.playerNicknameEntry.grid(row=0,column=1,sticky="w")
        self.submit = Button(self.playerSelector,text="Submit", relief = GROOVE,command=self.nameCheckerToGraph)
        self.submit.grid(row=1,column=0)
        self.back = Button(self.playerSelector, text="Main Menu", relief = GROOVE,command=self.nameCheckerToMenu)
        self.back.grid(row=1,column=1)

    def nameCheckerToMenu(self):
        self.playerSelector.destroy()
        self.mainMenu()
    
    def nameCheckerToGraph(self):
        self.playerNickname = self.playerNicknameEntry.get()
        cursor.execute("SELECT PlayerID,Nickname,Nationality FROM Player WHERE Nickname = (?) COLLATE NOCASE",(self.playerNickname,))
        player=cursor.fetchall()
        if len(player)==1:
            self.playerSelector.destroy()
            self.graph(player[0][0])
        elif len(player) <1:
            messagebox.showerror("Incorrect Name","The name you have selected doesn't exist in the database")
        else:
            self.playerSelector.destroy()
            self.playerSelector = Frame(self.master)
            self.playerSelector.grid()
            radioButtonValueList = []
            for each in player:
                radioButtonValueList.append([str(each[1]+ " " +each[2]),each[0]])
            print(radioButtonValueList)
            self.v = StringVar()
            self.v.set("L") # initialize
            for text, mode in radioButtonValueList:
                self.b = Radiobutton(self.playerSelector, text=text, variable=self.v, value=mode, indicatoron=0, command = self.multiNameToGraph)
                self.b.pack(anchor=W)

    def multiNameToGraph(self):
        self.playerSelector.destroy()
        self.graph(self.v.get())

    def graphToMainMenu(self):
        self.buttons.destroy()
        self.canvas.destroy()
        self.mainMenu()
        
        


root = Tk() #makes a blank window
##root.geometry("512x512")#Dimensions of window

app = Window(root)#Can hold oter widgets
app.mainMenu()
#when creating a widget always pass its owner/master
root.mainloop()#Now awaits events to handle
