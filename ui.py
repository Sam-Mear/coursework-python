from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview,Separator
import sqlite3,turtle
from datetime import date, timedelta, datetime
import updatePlayerTeams as UPT
from math import sqrt
from threading import Thread
import os.path

def checkIfDatabaseExists():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")# get all the table names of the database
    if cursor.fetchall() == [('Team',), ('Player',), ('Event',), ('Game',), ('GameMap',), ('PlayerMap',), ('TeamMap',)]:
        return(True)
    else:
        return(False)

class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)# Use the constructor
        #OR super().__init__(master)
        self.master = master

        self.master.title("CS Stats")
        self.master.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CSStats.ico"))
        self.todaysDate = date(2020, 3, 17)
        self.date90 = self.todaysDate - timedelta(90)
        self.date60 = self.todaysDate - timedelta(60)
        self.date30 = self.todaysDate - timedelta(30)
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
        self.manualResultEntry = Button(self.mainMenuFrame,text="Manual Result Entry", relief = GROOVE, command= self.manualResult)
        self.manualResultEntry.grid(row=1,column=0,sticky="s")
        self.mainMenuOtherFrame = Frame(self.mainMenuFrame)
        self.mainMenuOtherFrame.grid(row=0,column=1,rowspan=2)
        self.line = Separator(self.mainMenuOtherFrame,orient='vertical')
        self.line.grid(row=0,column=0,rowspan=5,sticky="NS",padx=5)

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
        self.selectPlayerButton = Button(self.mainMenuOtherFrame,text="Select Player", relief = GROOVE, command = self.mainMenuToGraph)
        self.selectPlayerButton.grid(row=4,column=2)

    def manualResult(self):
        self.mainMenuFrame.destroy()
        self.manualResultFrame = Frame(self.master)
        self.manualResultFrame.grid()
        self.title = Label(self.manualResultFrame, text="Manual Result Entry")
        self.title.grid(row=0,column=0)
        self.title.config(font=("Helvetica",11))
        self.subTitle = Label(self.manualResultFrame, text="First, select the event.")
        self.subTitle.grid(row=1,column=0)

        self.manualResultSubFrame = Frame(self.manualResultFrame)
        self.manualResultSubFrame.grid(row=2,column=0)
        self.eventNameEntryLabel = Label(self.manualResultSubFrame, text="Event Search:")
        self.eventNameEntryLabel.grid(row=0,column=0)
        self.eventNameEntry = Entry(self.manualResultSubFrame)
        self.eventNameEntry.grid(row=0,column=1)
        self.eventNameEntry.focus()
        self.eventNameSubmit = Button(self.manualResultSubFrame, text="Search", command=self.updateEventSearch)
        self.eventNameSubmit.grid(row=0,column=2)
        #################
        self.searchResultsLabel = Label(self.manualResultFrame,text="Event name search results:")
        self.searchResultsLabel.grid(row=3,column=0)
        self.searchResults = Listbox(self.manualResultFrame)
        self.searchResults.grid(row=4,column=0)
        self.selectSearch = Button(self.manualResultFrame, text="Select event", command=self.manualResultGame)
        self.selectSearch.grid(row=5,column=0)
        self.addNewEventButton = Button(self.manualResultFrame, text="Add a new event", command=self.addNewEvent)
        self.addNewEventButton.grid(row=6,column=0)
        self.mainMenuButton = Button(self.manualResultFrame, text="Main Menu", relief = GROOVE, command=self.manualResultToMainMenu)
        self.mainMenuButton.grid(row=7,column=0)
    
    def manualResultGame(self):
        if len(self.searchResults.curselection()) == 0:
            messagebox.showerror("No event selected","An event must be selected to enter a result")
        else:
            self.eventInfo = self.recentEventResult[self.searchResults.curselection()[0]]
            self.manualResultFrame.destroy()
            self.manualResultFrame = Frame(self.master)
            self.manualResultFrame.grid()
            self.title = Label(self.manualResultFrame, text="Manual Result Entry\nMatch Information")
            self.title.grid(row=0,column=0)
            self.title.config(font=("Helvetica",11))
            self.numberOfMapsLabel = Label(self.manualResultFrame, text="Number of maps:")
            self.numberOfMapsLabel.grid(row=0,column=1)
            self.format = StringVar()
            Radiobutton(self.manualResultFrame, text="Best of One", variable = self.format, value="Best of 1", command=self.enableNumberOfMaps).grid(row=1,column=0)
            Radiobutton(self.manualResultFrame, text="Best of Two", variable = self.format, value="Best of 2", command=self.enableNumberOfMaps).grid(row=2,column=0)
            Radiobutton(self.manualResultFrame, text="Best of Three", variable = self.format, value="Best of 3", command=self.enableNumberOfMaps).grid(row=3,column=0)
            Radiobutton(self.manualResultFrame, text="Best of Five", variable = self.format, value="Best of 5", command=self.enableNumberOfMaps).grid(row=4,column=0)
            self.format.set("Best of 1")
            self.radioButtonFrame = Frame(self.manualResultFrame)
            self.radioButtonFrame.grid(row=1,column=1,rowspan=4)
            self.numberOfMaps = StringVar()
            Radiobutton(self.radioButtonFrame, text="One", variable = self.numberOfMaps, value="1").grid()
            self.numberOfMaps.set("1")
            self.manualResultSubFrame = Frame(self.manualResultFrame)
            self.manualResultSubFrame.grid(row=5,column=0,columnspan=2)
            self.dateLabel = Label(self.manualResultSubFrame,text="Input date of match\nyyyy-mm-dd")
            self.dateLabel.grid(row=0,column=0,columnspan=2)
            self.yearLabel = Label(self.manualResultSubFrame,text="Year")
            self.yearLabel.grid(row=1,column=0,sticky="e")
            self.monthLabel = Label(self.manualResultSubFrame, text="Month")
            self.monthLabel.grid(row=1,column=1)
            self.dayLabel = Label(self.manualResultSubFrame, text="Day")
            self.dayLabel.grid(row=1,column=2,sticky="w")
            vcmd = (self.register(self.onValidate),'%S')#%S is the current character the user is trying to input. It calls the subroutine on validate, to check if the inputted character is a number. Only numbers are allowed to be inputted
            self.year = Entry(self.manualResultSubFrame, validate="key",validatecommand=vcmd,width=4)
            self.year.grid(row=2,column=0,sticky="e")
            self.month = Entry(self.manualResultSubFrame, validate="key",validatecommand=vcmd,width=2)
            self.month.grid(row=2,column=1)
            self.day = Entry(self.manualResultSubFrame, validate="key",validatecommand=vcmd,width=2)
            self.day.grid(row=2,column=2,sticky="w")
            self.submit = Button(self.manualResultFrame, text="Submit",command=self.gameDatabaseEntry)
            self.submit.grid(row=6,column=0,columnspan=2)

    def gameDatabaseEntry(self):
        if len(self.year.get()) == 4:#Checking the year is 4 values, cant be in the ear 211 or 24442
            if len(self.month.get()) ==2:#Checking the month is 2 digits so it cant be 1 or 122, has to be 12 or 01
                if len(self.day.get())==2:#Same check as above
                    #if messagebox.askquestion("Are you sure","Are you sure you want to apply this change? This will alter the data stored in the database, and can only be reversed manually") == 'yes':                        
                    cursor.execute("INSERT INTO Game (Format,NumberOfMaps,Date,EventID) VALUES (?,?,?,?)",(self.format.get(), self.numberOfMaps.get(), "{0}-{1}-{2}".format(self.year.get(),self.month.get(),self.day.get()), self.eventInfo[0]))
                        #cursor.execute("COMMIT")FINDME#ONLY COMMIT AT END
                    messagebox.showinfo("Done","Moving onto the maps")
                    self.mapDatabaseUIIndex = 0#This is the index, counting how many maps has been inputted, when this matches the number of maps, which the user gave earlier, it will stop prompting the user to give new map data as it has now finished.
                    self.numberOfMaps = self.numberOfMaps.get()
                    self.gameID = cursor.lastrowid#Gets GameID of the most recent INSERT
                    self.mapDatabaseUI()
                    #else:
                    #    messagebox.showinfo("No database change","There has been no database altering")
                else:
                    messagebox.showerror("Day Entry Error","The day box must be 2 characters long.")
            else:
                messagebox.showerror("Month Entry Error","The month box must be 2 characters long.")
        else:
            messagebox.showerror("Year Entry Error","The year box must be 4 characters long.")
    
    def mapDatabaseUI(self):
        self.mapDatabaseUIIndex += 1
        vcmd = (self.register(self.onValidate),'%S')#%S is the current character the user is trying to input. It calls the subroutine on validate, to check if the inputted character is a number. Only numbers are allowed to be inputted
            #entry
        self.manualResultFrame.destroy()
        self.manualResultFrame = Frame(self.master)
        self.manualResultFrame.grid()
        self.mapNameLabel = Label(self.manualResultFrame, text="Map Name:")
        self.mapNameLabel.grid(row=0,column=0, sticky="e")
        self.roundsPlayedLabel = Label(self.manualResultFrame, text="Rounds Played:")
        self.roundsPlayedLabel.grid(row=1,column=0,sticky="e")
        self.mapNameEntry = Entry(self.manualResultFrame)
        self.mapNameEntry.grid(row=0,column=1,sticky="w")
        self.mapNameEntry.focus()
        self.roundsPlayedEntry = Entry(self.manualResultFrame,validate="key",validatecommand=vcmd)
        self.roundsPlayedEntry.grid(row=1,column=1,sticky="w")
        self.submit = Button(self.manualResultFrame, text="Submit",command= lambda: self.mapDatabaseEntry())
        self.submit.grid(row=2,column=0,columnspan=2)
    
    def mapDatabaseEntry(self):
        if len(self.mapNameEntry.get()) > 0:#Making sure th input box isnt left empty
            if len(self.roundsPlayedEntry.get()) > 0:#Making sure th input box isnt left empty
                cursor.execute("INSERT INTO GameMap (RoundsPlayed,MapName,GameID) VALUES (?,?,?)",(self.roundsPlayedEntry.get(),self.mapNameEntry.get(),self.gameID))
                self.mapID = cursor.lastrowid
                self.teamMapDatabaseUIWinning()
            else:
                messagebox.showerror("Rounds Played Empty","The rounds played entry must not be empty.")
        else:
            messagebox.showerror("Map Name Empty","The map name entry must not be empty.")
    
    def teamMapDatabaseUIWinning(self):
        self.manualResultFrame.destroy()
        self.manualResultFrame = Frame(self.master)
        self.manualResultFrame.grid()
        self.teamNameEntryLabel = Label(self.manualResultFrame, text="Winning team Search:")
        self.teamNameEntryLabel.grid(row=0,column=0, sticky="e")
        self.teamNameEntry = Entry(self.manualResultFrame)
        self.teamNameEntry.grid(row=0,column=1,sticky = "w")
        self.teamNameEntry.focus()
        self.teamNameSubmit = Button(self.manualResultFrame, text="Search", command=self.updateTeamSearch)
        self.teamNameSubmit.grid(row=0,column=2,sticky="w")
        self.searchResultsLabel = Label(self.manualResultFrame,text="Winning team name search results:")
        self.searchResultsLabel.grid(row=1,column=0,columnspan=3)
        self.searchResults = Listbox(self.manualResultFrame)
        self.searchResults.grid(row=2,column=0,columnspan=3)
        vcmd = (self.register(self.onValidate),'%S')#%S is the current character the user is trying to input. It calls the subroutine on validate, to check if the inputted character is a number. Only numbers are allowed to be inputted
        self.roundsWonLabel = Label(self.manualResultFrame, text="Rounds Won:")
        self.roundsWonLabel.grid(row=3,column=0,sticky="e")
        self.roundsWonEntry = Entry(self.manualResultFrame, validate="key",validatecommand=vcmd)
        self.roundsWonEntry.grid(row=3,column=1,sticky="w")
        self.roundsLostLabel = Label(self.manualResultFrame, text="Rounds Lost:")
        self.roundsLostLabel.grid(row=4,column=0,sticky="e")
        self.roundsLostEntry = Entry(self.manualResultFrame, validate="key",validatecommand=vcmd)
        self.roundsLostEntry.grid(row=4,column=1,sticky="w")
        self.submit = Button(self.manualResultFrame, text="Submit Data", command=self.teamMapDatabaseUIManagerWinning)
        self.submit.grid(row=5,column=0,columnspan=3)

    def teamMapDatabaseUIManagerWinning(self):
        if len(self.searchResults.curselection()) > 0:
            if len(self.roundsWonEntry.get()) == 0:#Making sure the input box isnt left empty
                messagebox.showerror("Rounds won empty","The rounds won entry box cannot be empty!")
            elif len(self.roundsLostEntry.get()) == 0:#Making sure the input box isnt left empty
                messagebox.showerror("Rounds lost empty","The rounds lost entry box cannot be empty!")
            elif int(self.roundsWonEntry.get()) <= int(self.roundsLostEntry.get()):#Making sure the winning team has more rounds won than rounds lost
                messagebox.showerror("Error","You are selecting the winning team, so this team must have more rounds won than rounds lost.")
            else:#When it has parsed all its verification checks...
                self.winningTeam = self.recentTeamResult[self.searchResults.curselection()[0]][0]
                cursor.execute("INSERT INTO TeamMap (GameMapID,TeamID,Won,RoundsWon,RoundsLost) VALUES (?,?,?,?,?)",(self.mapID,self.winningTeam,"w",self.roundsWonEntry.get(),self.roundsLostEntry.get(),))
                self.teamMapDatabaseUILosing()# onto next page...
        else:
            messagebox.showerror("Nothing selected","You must have something selected when adding a selected team")
    
    def teamMapDatabaseUILosing(self):
        self.manualResultFrame.destroy()#destroys ui for
        self.manualResultFrame = Frame(self.master)#new ui. Buttons and ui elements will be applied to this frame
        self.manualResultFrame.grid()
        self.teamNameEntryLabel = Label(self.manualResultFrame, text="Losing team Search:")
        self.teamNameEntryLabel.grid(row=0,column=0, sticky="e")
        self.teamNameEntry = Entry(self.manualResultFrame)
        self.teamNameEntry.grid(row=0,column=1,sticky = "w")
        self.teamNameEntry.focus()
        self.teamNameSubmit = Button(self.manualResultFrame, text="Search", command=self.updateTeamSearch)
        self.teamNameSubmit.grid(row=0,column=2,sticky="w")
        self.searchResultsLabel = Label(self.manualResultFrame,text="Losing team name search results:")
        self.searchResultsLabel.grid(row=1,column=0,columnspan=3)
        self.searchResults = Listbox(self.manualResultFrame)
        self.searchResults.grid(row=2,column=0,columnspan=3)
        vcmd = (self.register(self.onValidate),'%S')#%S is the current character the user is trying to input. It calls the subroutine on validate, to check if the inputted character is a number. Only numbers are allowed to be inputted
        self.roundsWonLabel = Label(self.manualResultFrame, text="Rounds Won:")
        self.roundsWonLabel.grid(row=3,column=0,sticky="e")
        self.roundsWonEntry = Entry(self.manualResultFrame, validate="key",validatecommand=vcmd)
        self.roundsWonEntry.grid(row=3,column=1,sticky="w")
        self.roundsLostLabel = Label(self.manualResultFrame, text="Rounds Lost:")
        self.roundsLostLabel.grid(row=4,column=0,sticky="e")
        self.roundsLostEntry = Entry(self.manualResultFrame, validate="key",validatecommand=vcmd)
        self.roundsLostEntry.grid(row=4,column=1,sticky="w")
        self.submit = Button(self.manualResultFrame, text="Submit Data", command=self.teamMapDatabaseUIManagerLosing)
        self.submit.grid(row=5,column=0,columnspan=3)

    def teamMapDatabaseUIManagerLosing(self):
        if len(self.searchResults.curselection()) > 0:
            if len(self.roundsWonEntry.get()) == 0:
                messagebox.showerror("Rounds won empty","The rounds won entry box cannot be empty!")
            elif len(self.roundsLostEntry.get()) == 0:
                messagebox.showerror("Rounds lost empty","The rounds lost entry box cannot be empty!")
            elif int(self.roundsWonEntry.get()) >= int(self.roundsLostEntry.get()):
                messagebox.showerror("Error","You are selecting the losing team, so this team must have more rounds lost than rounds won.")
            elif self.winningTeam == self.recentTeamResult[self.searchResults.curselection()[0]][0]:#.curselection returns an index, so i have saved the search results as a list, so i can use the index to find out what value the user has selected.
                messagebox.showerror("Winning team cant be losing team","Team 2 cannot be team 1, they must be different teams.")
            else:
                self.losingTeam = self.recentTeamResult[self.searchResults.curselection()[0]][0]
                cursor.execute("INSERT INTO TeamMap (GameMapID,TeamID,Won,RoundsWon,RoundsLost) VALUES (?,?,?,?,?)",(self.mapID,self.losingTeam,"l",self.roundsWonEntry.get(),self.roundsLostEntry.get(),))
                self.manualResultDone()
        else:
            messagebox.showerror("Nothing selected","You must have something selected when adding a selected team")
    
    def manualResultDone(self):
        if int(self.mapDatabaseUIIndex) > int(self.numberOfMaps):#not all maps entered:
            if messagebox.askquestion("Confirm","Manual result entering is done. This is final confirm to apply changes to the database.\nAre you sure?") =="yes":
                cursor.execute("COMMIT")#applys the chanages.
            else:
                messagebox.showinfo("No changes","No changes were made")
            self.manualResultToMainMenu()
        else:#if all maps entered
            self.mapDatabaseUI()
    
    def onValidate(self,S):
        # Disallow anything but numbers
        if S.isdigit() == True:
            return True#ays that character can be entered.
        else:
            self.bell()#gives sound queu that, that character cannot be entered.
            return False#says that character cannot be entered
    
    def enableNumberOfMaps(self):
        self.radioButtonFrame.destroy()
        self.radioButtonFrame = Frame(self.manualResultFrame)
        self.radioButtonFrame.grid(row=1,column=1,rowspan=4)
        if self.format.get() == "Best of 1":
            self.numberOfMaps = StringVar()
            Radiobutton(self.radioButtonFrame, text="One", variable = self.numberOfMaps, value="1").grid()
            self.numberOfMaps.set("1")
        elif self.format.get() == "Best of 3":
            self.numberOfMaps = StringVar()
            Radiobutton(self.radioButtonFrame, text="Two", variable = self.numberOfMaps, value="2").grid()
            Radiobutton(self.radioButtonFrame, text="Three", variable = self.numberOfMaps, value="3").grid()
            self.numberOfMaps.set("3")
        elif self.format.get() == "Best of 5":
            self.numberOfMaps = StringVar()
            Radiobutton(self.radioButtonFrame, text="Three", variable = self.numberOfMaps, value="3").grid()
            Radiobutton(self.radioButtonFrame, text="Four", variable = self.numberOfMaps, value="4").grid()
            Radiobutton(self.radioButtonFrame, text="Five", variable = self.numberOfMaps, value="5").grid()
            self.numberOfMaps.set("5")
        else:
            self.numberOfMaps = StringVar()
            Radiobutton(self.radioButtonFrame, text="Two", variable = self.numberOfMaps, value="2").grid()
            self.numberOfMaps.set("2")
    
    def addNewEvent(self):
        self.manualResultFrame.destroy()
        self.manualResultFrame =Frame(self.master)
        self.manualResultFrame.grid()
        self.eventNameLabel = Label(self.manualResultFrame,text="Event Name:")
        self.eventNameEntry = Entry(self.manualResultFrame)
        self.eventNameEntry.focus()
        self.eventNameLabel.grid(row=0,column=0,sticky="e")
        self.eventNameEntry.grid(row=0,column=1,sticky="w")
        self.submit = Button(self.manualResultFrame,text="Submit", relief = GROOVE,command=self.eventDatabaseEntry)
        self.submit.grid(row=1,column=0)
        self.back = Button(self.manualResultFrame, text="Main Menu", relief = GROOVE,command=self.manualResultToMainMenu)
        self.back.grid(row=1,column=1)

    def eventDatabaseEntry(self):
        if messagebox.askquestion("Are you sure","Are you sure you want to apply this change? This will alter the data stored in the database, and can only be reversed manually") == 'yes':
            if self.eventNameEntry.get() == "":
                messagebox.showerror("No event name","You must enter an event name")
            else:
                cursor.execute("SELECT * FROM Event WHERE EventName = (?)",(self.eventNameEntry.get(),))
                if len(cursor.fetchall()) > 0:
                    messagebox.showerror("Event exists","An event with this event name already exists")
                else:
                    cursor.execute("INSERT INTO Event (EventName) VALUES (?)",(self.eventNameEntry.get(),))
                    cursor.execute("COMMIT")
                    messagebox.showinfo("Done","The event has been added to the database")
                    self.manualResultToMainMenu()
        else:
            messagebox.showinfo("No database change","There has been no database altering")

    def updateEventSearch(self):
        if self.eventNameEntry.get() == "":#if nothing is entered
            messagebox.showerror("Nothing entered","You must have something entered when searching for events")
        else:
            cursor.execute("SELECT * FROM Event WHERE EventName LIKE (?)",("%"+str(self.eventNameEntry.get())+"%",))#does the search by sql
            self.recentEventResult = cursor.fetchall()#fetches the data from the search.
            #The data needs to be stored like this because when you do curselection() on the list box, it returns an index, so with that index and this list^i can find out which search iten the user has selected
            self.searchResults.delete(0,END)#removes previous search result
            for i in self.recentEventResult:
                self.searchResults.insert(END,i[1])# and inserts the new search results into the list box

    def manualResultToMainMenu(self):
        self.manualResultFrame.destroy()
        self.mainMenu()

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
            self.playerList = []
            linRegPredictionList = []
            for each in self.selectedTeamsList:#For each selected team
                cursor.execute("SELECT NSPlayerID, Player.Nickname, round(((((STRating - TNRating)+ratingDifferenceNSST)/2)*-1),2) FROM( SELECT NSPlayerID, (NSRating - STRating) ratingDifferenceNSST, NSRating, STRating FROM ( SELECT PlayerMap.PlayerID NSPlayerID, avg(Rating) NSRating FROM PlayerMap, Player, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Player.PlayerID = PlayerMap.PlayerID AND Player.TeamID IN(?) AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerMap.PlayerID), ( SELECT PlayerMap.PlayerID STPlayerID, avg(Rating) STRating FROM PlayerMap, Player, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Player.PlayerID = PlayerMap.PlayerID AND Player.TeamID IN(?) AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerMap.PlayerID ) WHERE NSPlayerID = STPlayerID ), ( SELECT PlayerMap.PlayerID TNPlayerID, avg(Rating) TNRating FROM PlayerMap, GameMap, Player, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Player.PlayerID = PlayerMap.PlayerID AND Player.TeamID IN(?) AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerMap.PlayerID ), Player WHERE NSPlayerID = TNPlayerID AND NSPlayerID = Player.PlayerID",(each[0],self.date90,self.date60,each[0],self.date60,self.date30,each[0],self.date30,self.todaysDate))
                for Each in cursor.fetchall():#For each player
                    if len(Each) > 0:#If not empty -  can happen when player doesnt play for a month.
                        cursor.execute("SELECT PlayerID, avg(Rating) FROM PlayerMap, GameMap,Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND Game.GameID = GameMap.GameID AND Date > (?) AND PlayerID = (?)",(self.date90, Each[0]))
                        temp = cursor.fetchall()
                        self.playerList.append([temp[0][0],temp[0][1]+Each[2]])
                        #LinReg part
                        #for simplicity in reading, ive made it a separate subroutine
                        linRegPredictionList.append([Each[1],self.linRegPredictionSubroutine(Each[0])])
            playersOnRisePrediction = [0,0.0]
            linRegPrediction = ["",0.0]
            for i in range(len(self.playerList)):
                if playersOnRisePrediction[1] <self.playerList[i][1]:
                    playersOnRisePrediction = self.playerList[i]
                if linRegPrediction[1] < linRegPredictionList[i][1]:
                    linRegPrediction = linRegPredictionList[i]
            cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(str(playersOnRisePrediction[0]),))
            playersOnRisePrediction[0]=cursor.fetchall()[0][0]
            playersOnRisePrediction[1] = round(playersOnRisePrediction[1],2)
            linRegPrediction[1] = round(linRegPrediction[1],2)
            self.eventMVPPredictorFrame.destroy()
            self.eventMVPPredictorFrame = Frame(self.master)
            self.eventMVPPredictorFrame.grid()
            self.title = Label(self.eventMVPPredictorFrame, text="Event MVP Predictor")
            self.title.grid(row=0,column=0, columnspan=2)
            self.title.config(font=("Helvetica",11))
            self.playersRiseLabel = Label(self.eventMVPPredictorFrame, text="Players On Rise Prediction: ")
            self.playersRiseLabel.grid(row=1,column=0)
            self.playersRisePrediction = Label(self.eventMVPPredictorFrame, text=str(playersOnRisePrediction[0])+": "+str(playersOnRisePrediction[1])+" rating")
            self.playersRisePrediction.grid(row=1,column=1)
            self.linRegPredictionLabel = Label(self.eventMVPPredictorFrame, text="Linear Regression Prediction: ")
            self.linRegPredictionLabel.grid(row=2,column=0)
            self.linRegPrediction = Label(self.eventMVPPredictorFrame,text=str(linRegPrediction[0])+": "+str(linRegPrediction[1])+" rating")
            self.linRegPrediction.grid(row=2,column=1)
            self.mainMenuButton = Button(self.eventMVPPredictorFrame, text="Main Menu", command=self.eventPredictToMain)
            self.mainMenuButton.grid(row=3,column=0,columnspan=2)
            #get coords if it were to be on a graph
            #linear regression to find out what rating would be in 15 days
            #
            #predict b is my players on the rise thing, but it finds the difference between the different
            #bits and predicts next 15 days from that.
        else:
            messagebox.showerror("No Teams","There must be at least two teams selected.")

    def linRegPredictionSubroutine(self,playerID):
        cursor.execute("SELECT Game.Date, Rating FROM PlayerMap, GameMap, Game WHERE PlayerID = (?) AND PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) ORDER BY Date DESC",(playerID,str(self.date90)))
        playerRatings = cursor.fetchall()
        playerRatingsDate = []
        self.coords = []
        for i in range(len(playerRatings)):
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
        n=len(self.coords)
        sumX = 0
        sumY = 0
        sumXSquared = 0
        sumXY = 0
        for i in range(n):
            sumX += self.coords[i][0]
            sumY += self.coords[i][1]
            sumXSquared += self.coords[i][0]**2
            sumXY += self.coords[i][0]*self.coords[i][1]
        #y=bx+a
        sxy = sumXY-((sumX*sumY)/n)
        sxx = sumXSquared-(sumX**2/n)
        b = sxy/sxx
        a=(sumY/n) - ((sumX/n)*b)
        y = b*420+a
        return((y/300)+1)

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
        if self.teamNameEntry.get() == "":# checks if a search has been entered
            messagebox.showerror("Nothing entered","You must have something entered when searching for teams")
        else:#if yes
            cursor.execute("SELECT * FROM Team WHERE TeamName LIKE (?)",("%"+str(self.teamNameEntry.get())+"%",))#performs search by SQL
            self.recentTeamResult = cursor.fetchall()#fetches the data
            #The data needs to be stored like this because when you do curselection() on the list box, it returns an index, so with that index and this list^i can find out which search iten the user has selected
            self.searchResults.delete(0,END)#removes previous search results
            for i in self.recentTeamResult:#updates listbox with the new search results
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
        self.manual = Button(self.updatePlayerTeamsFrame, text="Manual", relief = GROOVE, command=self.playerTeamsManual)
        self.manual.grid(row=1,column=1)
        self.mainMenuButton = Button(self.updatePlayerTeamsFrame, text="Main Menu", relief = GROOVE, command=self.playerTeamsToMainMenu)
        self.mainMenuButton.grid(row=2,column=0,columnspan=2)
    
    def playerTeamsManual(self):
        self.updatePlayerTeamsFrame.destroy()
        self.updatePlayerTeamsFrame = Frame(self.master)
        self.updatePlayerTeamsFrame.grid()
        self.title = Label(self.updatePlayerTeamsFrame, text="Update Player's Teams")
        self.title.grid(row=0,column=0)
        self.title.config(font=("Helvetica",11))

        self.updatePlayerTeamsSubFrame = Frame(self.updatePlayerTeamsFrame)
        self.updatePlayerTeamsSubFrame.grid(row=1,column=0)
        self.playerNameEntryLabel = Label(self.updatePlayerTeamsSubFrame, text="Player Search:")
        self.playerNameEntryLabel.grid(row=0,column=0)
        self.playerNameEntry = Entry(self.updatePlayerTeamsSubFrame)
        self.playerNameEntry.grid(row=0,column=1)
        self.playerNameEntry.focus()
        self.playerNameSubmit = Button(self.updatePlayerTeamsSubFrame, text="Search", command=self.updatePlayerSearch)
        self.playerNameSubmit.grid(row=0,column=2)
        ################
        self.searchResultsLabel = Label(self.updatePlayerTeamsFrame,text="Player name search results:")
        self.searchResultsLabel.grid(row=2,column=0)
        self.searchResults = Listbox(self.updatePlayerTeamsFrame)
        self.searchResults.grid(row=3,column=0)
        self.selectSearch = Button(self.updatePlayerTeamsFrame, text="Select player", command= self.changePlayerTeam)
        self.selectSearch.grid(row=4,column=0)
        self.mainMenuButton = Button(self.updatePlayerTeamsFrame, text="Main Menu", relief = GROOVE, command=self.playerTeamsToMainMenu)
        self.mainMenuButton.grid(row=5,column=0)
    
    def changePlayerTeam(self):
        if len(self.searchResults.curselection()) > 0:
            self.player = self.recentPlayerResult[self.searchResults.curselection()[0]]
            self.updatePlayerTeamsFrame.destroy()
            self.updatePlayerTeamsFrame = Frame(self.master)
            self.updatePlayerTeamsFrame.grid()
            self.title = Label(self.updatePlayerTeamsFrame, text="Update Player's Teams\nPlayerName = " + self.player[1])
            self.title.grid(row=0,column=0)
            self.title.config(font=("Helvetica",11))
            cursor.execute("SELECT TeamName FROM Team WHERE TeamID = (?)",(self.player[3],))
            self.subTitle = Label(self.updatePlayerTeamsFrame, text="Current team: "+str(cursor.fetchall()[0][0]))
            self.subTitle.grid(row=1,column=0)

            self.updatePlayerTeamsSubFrame = Frame(self.updatePlayerTeamsFrame)
            self.updatePlayerTeamsSubFrame.grid(row=2,column=0)
            self.teamNameEntryLabel = Label(self.updatePlayerTeamsSubFrame, text="Team Search:")
            self.teamNameEntryLabel.grid(row=0,column=0)
            self.teamNameEntry = Entry(self.updatePlayerTeamsSubFrame)
            self.teamNameEntry.grid(row=0,column=1)
            self.teamNameEntry.focus()
            self.teamNameSubmit = Button(self.updatePlayerTeamsSubFrame, text="Search", command=self.updateTeamSearch)
            self.teamNameSubmit.grid(row=0,column=2)
            #################
            self.searchResultsLabel = Label(self.updatePlayerTeamsFrame,text="Team name search results:")
            self.searchResultsLabel.grid(row=3,column=0)
            self.searchResults = Listbox(self.updatePlayerTeamsFrame)
            self.searchResults.grid(row=4,column=0)
            self.selectSearch = Button(self.updatePlayerTeamsFrame, text="Select team", command = self.applyChange)
            self.selectSearch.grid(row=5,column=0)
            self.mainMenuButton = Button(self.updatePlayerTeamsFrame, text="Main Menu", relief = GROOVE, command=self.playerTeamsToMainMenu)
            self.mainMenuButton.grid(row=6,column=0)
        else:
            messagebox.showerror("Nothing selected","You must have a player selected.")

    def applyChange(self):
        if len(self.searchResults.curselection()) > 0:
            if messagebox.askquestion("Are you sure","Are you sure you want to apply this change? This will alter the data stored in the database, and can only be reversed manually") == 'yes':
                #perform the changes
                print(self.player)
                print(self.recentTeamResult[self.searchResults.curselection()[0]][0])
                cursor.execute("UPDATE Player SET TeamID = (?) WHERE PlayerID = (?)",(self.recentTeamResult[self.searchResults.curselection()[0]][0],self.player[0]))
                cursor.execute("COMMIT")
                messagebox.showinfo("Done","Changes were saved")
                self.playerTeamsToMainMenu()
            else:
                messagebox.showinfo("No changes","You did not apply any changes")
        else:
            messagebox.showerror("Nothing selected","You must have a team selected.")
 
    def updatePlayerSearch(self):
        if self.playerNameEntry.get() == "":
            messagebox.showerror("Nothing entered","You must have something entered when searching for players")
        else:#Checks if anything was entered into the search box
            cursor.execute("SELECT * FROM Player WHERE Nickname LIKE (?)",("%"+str(self.playerNameEntry.get())+"%",))#performs search via sql
            self.recentPlayerResult = cursor.fetchall()
            #The data needs to be stored like this because when you do curselection() on the list box, it returns an index, so with that index and this list^i can find out which search iten the user has selected
            self.searchResults.delete(0,END)
            for i in self.recentPlayerResult:
                self.searchResults.insert(END,i[1])

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
            cursor.execute("SELECT NSPlayerID,  Player.Nickname, (STRating - TNRating) ratingDifference FROM (SELECT NSPlayerID, (NSRating - STRating), NSRating, STRating FROM (SELECT PlayerID NSPlayerID, avg(Rating) NSRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),(SELECT PlayerID STPlayerID, avg(Rating) STRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID) WHERE NSPlayerID = STPlayerID AND (NSRating - STRating) < -0.15),(SELECT PlayerID TNPlayerID, avg(Rating) TNRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),Player WHERE NSPlayerID = TNPlayerID AND ratingDifference < -0.15 AND NSPlayerID = Player.PlayerID ORDER BY ratingDifference ASC LIMIT 10",(self.date90,self.date60,self.date60,self.date30,self.date30,self.todaysDate))
            self.title = Label(self.playersFrame, text="Players on the Rise")
        else:
            cursor.execute("SELECT NSPlayerID,  Player.Nickname, (STRating - TNRating) ratingDifference FROM (SELECT NSPlayerID, (NSRating - STRating), NSRating, STRating FROM (SELECT PlayerID NSPlayerID, avg(Rating) NSRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),(SELECT PlayerID STPlayerID, avg(Rating) STRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID) WHERE NSPlayerID = STPlayerID AND (NSRating - STRating) > 0.15),(SELECT PlayerID TNPlayerID, avg(Rating) TNRating FROM PlayerMap, GameMap, Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) AND Game.Date <= (?) GROUP BY PlayerID),Player WHERE NSPlayerID = TNPlayerID AND ratingDifference > 0.15 AND NSPlayerID = Player.PlayerID ORDER BY ratingDifference DESC LIMIT 10",(self.date90,self.date60,self.date60,self.date30,self.date30,self.todaysDate))
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
            messagebox.showerror("No selection","No selection was made")

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

        self.mapsTreeview = Treeview(self.teamsFrame, height=10)
        self.mapsTreeview.grid(row=1,column=0,columnspan=2)
        self.mapsTreeview["columns"]=("Maps","Total Maps")
        self.mapsTreeview.column("#0", width=120, minwidth=120, stretch=True)
        self.mapsTreeview.column("Maps", width=140, minwidth=140, stretch=True)
        self.mapsTreeview.column("Total Maps", width=75, minwidth=75, stretch=True)
        self.mapsTreeview.heading("#0",text="Team Name")
        self.mapsTreeview.heading("Maps",text="Maps Won - Maps Lost")
        self.mapsTreeview.heading("Total Maps",text="Total Maps")

        self.backButton = Button(self.teamsFrame,text="Back to Main Menu", relief = GROOVE, command=self.teamsToMainMenu)
        self.backButton.grid(row=0,column=1,sticky="e")
        un = 0
        for i in range(len(self.teamsWLResult)):
            splittedString = str(self.teamsWLResult[i]).split(",")
            self.mapsTreeview.insert("", END, un, text=splittedString[0].split("'")[1], values=(splittedString[1],splittedString[2].split(")")[0]))
            un = un+1

    def teamsToMainMenu(self):
        self.teamsFrame.destroy()
        self.mainMenu()

    def eventMVPPicker(self):
        self.mainMenuFrame.destroy()#Destroys old frame
        self.eventMVPPickerFrame = Frame(self.master)#to make way for the new frame
        self.eventMVPPickerFrame.grid()
        cursor.execute("SELECT EventName, Event.EventID FROM Event, Game WHERE Date > (?) AND  Game.EventID = Event.EventID GROUP BY EventName",(self.todaysDate - timedelta(20),))
        self.eventNamesQRY = cursor.fetchall()#all results from above query
        self.eventNames = Listbox(self.eventMVPPickerFrame,height = (len(self.eventNamesQRY)+1),width = 70)#the hight of this listbox is dependant on how many results we get from the above query
        self.eventNames.grid(row=0,column=0)
        self.eventNames.insert(1, "EventName,EventID")
        for i in range(len(self.eventNamesQRY)):#inserting the values into the list box.
            self.eventNames.insert(i+2,str(self.eventNamesQRY[i]))
        self.buttonSelectEvent = Button(self.eventMVPPickerFrame,text="Select Event", relief = GROOVE,command = self.EventMVPSelection)
        self.buttonSelectEvent.grid(row=0,column=1)

    def EventMVPSelection(self):
        if len(self.eventNames.curselection())>0 and self.eventNames.curselection()[0] != 0:#If an event was selected
            eventID = self.eventNamesQRY[self.eventNames.curselection()[0]-1][1]#get the event ID
            eventName = self.eventNamesQRY[self.eventNames.curselection()[0]-1][0]#AND THE NAME
            self.eventMVPPickerFrame.destroy()#destroy the old ui, to make way for the new ui
            cursor.execute("SELECT round(AVERAGERATING,2),SUBQRYPLAYER FROM (SELECT avg(Rating) AVERAGERATING, PlayerID SUBQRYPLAYER FROM Event, Game, GameMap, PlayerMap WHERE Event.EventID = (?) AND Event.EventID = Game.EventID AND GameMap.GameID = Game.GameID AND PlayerMap.GameMapID = GameMap.GameMapID GROUP BY PlayerID ORDER BY avg(Rating) DESC LIMIT 5)",(eventID,))
            self.top5 = cursor.fetchall()#fetch all results from the query
            self.eventMVPSelectionFrame = Frame(self.master)#Make a new frame for the UI
            self.eventMVPSelectionFrame.grid()#grid it so it is in the UI
            self.title = Label(self.eventMVPSelectionFrame, text="Event: {0}".format(eventName),borderwidth=2, relief="groove")
            self.title.grid(row=0,column=0,columnspan=3)
            self.title.config(font=("Helvetica",11))


            #top5 players results
            self.top5Treeview = Treeview(self.eventMVPSelectionFrame, height=5)
            self.top5Treeview.grid(row=1,column=2,rowspan=4)
            self.top5Treeview["columns"]=("Team Name","Rating")
            self.top5Treeview.column("#0", width=100, minwidth=100, stretch=True)
            self.top5Treeview.column("Team Name", width=75, minwidth=75, stretch=True)
            self.top5Treeview.column("Rating", width=50, minwidth=50, stretch=True)
            self.top5Treeview.heading("#0",text="Player Name")
            self.top5Treeview.heading("Team Name",text="Team Name")
            self.top5Treeview.heading("Rating",text="Rating")

            self.temp = []
            un = 0
            for i in range(len(self.top5)):
                cursor.execute("SELECT Nickname, TeamName FROM Player,Team WHERE PlayerID = (?) AND Player.TeamID = Team.TeamID",(self.top5[i][1],))
                self.temp.append(cursor.fetchall())
                self.temp[i].append(self.top5[i][0])
                splittedString = str(self.temp[i]).split(",")
                self.top5Treeview.insert("", END, un, text=splittedString[0].split("'")[1], values=(splittedString[1].split("'")[1],splittedString[2].split("]")[0]))
                un=un+1
            self.eventStartLabel = Label(self.eventMVPSelectionFrame, text="Event Start Date:")
            self.eventStartLabel.grid(row=1,column=0,sticky=E)
            self.eventEndLabel = Label(self.eventMVPSelectionFrame, text="Event End Date:")
            self.eventEndLabel.grid(row=2,column=0,sticky=E)
            cursor.execute("SELECT min(Date),max(Date) FROM Game WHERE EventID = (?)",(eventID,))
            eventDates = cursor.fetchall()
            self.eventStart = Label(self.eventMVPSelectionFrame, text=eventDates[0][0])
            self.eventStart.grid(row=1,column=1,sticky=W)
            self.eventEnd = Label(self.eventMVPSelectionFrame, text=eventDates[0][1])
            self.eventEnd.grid(row=2,column=1,sticky=W)
            cursor.execute("SELECT Nickname, round(AVERAGERATING, 2) FROM (SELECT avg(Rating) AVERAGERATING, PlayerID SUBQRYPLAYER, count(TeamMap.Won) COUNTED FROM Event, Game, GameMap, PlayerMap, TeamMap WHERE Event.EventID = (?) AND Event.EventID = Game.EventID AND GameMap.GameID = Game.GameID AND TeamMap.GameMapID = GameMap.GameMapID AND PlayerMap.GameMapID = GameMap.GameMapID GROUP BY PlayerID ORDER BY avg(Rating) DESC LIMIT 10), Player WHERE SUBQRYPLAYER = Player.PlayerID ORDER BY COUNTED DESC LIMIT 1",(eventID,))
            self.reccomend = Label(self.eventMVPSelectionFrame, text="Program reccomedation:\n{0}".format(cursor.fetchall()))
            self.reccomend.grid(row=3,column=0,columnspan=2)
            self.backToMainMenu = Button(self.eventMVPSelectionFrame, text="Main Menu", relief = GROOVE,command=self.eventMVPPickerToMenu)
            self.backToMainMenu.grid(row=4,column=0,columnspan=2)
        else:
            messagebox.showerror("No selection","No event was selected!")#Show an error box, and dont change any ui elements.

    def eventMVPPickerToMenu(self):
        self.eventMVPSelectionFrame.destroy()
        self.mainMenu()
    
    def mainMenuToGraph(self):
        #making sure there is a selection, and that the selection is valid
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
            messagebox.showerror("ERROR","You didnt select a player!")

    def graph(self,playerID):
        print(playerID)
        cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(playerID,))
        playerName = cursor.fetchall()[0][0]
        cursor.execute("SELECT Game.Date, Rating FROM PlayerMap, GameMap, Game WHERE PlayerID = (?) AND PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) ORDER BY Date DESC",(playerID,str(self.date90)))
        playerRatings = cursor.fetchall()
        if len(playerRatings) == 0:#if they havent played a map in the past three months
            messagebox.showerror("Error","The player you have selected hasnt played a map in the past three months")
            self.mainMenu()#aaaaaaaa
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
        h,w=600,720#720 because i want it easily divisable by 90
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
        pen._tracer(0,0)#makes turtle even faster
        pen2._tracer(0,0)#makes turtle even faster
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
        pen.goto(-w//2+20,-20)
        pen.write("90 days ago")
        pen.goto(w//2-30,-20)
        pen.write("Now")
        pen.goto(20,-h//2+30)
        pen.write("Rating 0.00")
        pen.goto(20,h//2-30)
        pen.write("Rating 2.00")
        ########  self.coords  #################
        pen2.penup()
        for i in self.coords:
            pen2.goto(i)
            pen2.pendown()
            pen2.penup()
            pen2.fd(5)
            pen2.left(90)
            pen2.pendown()
            for j in range(60):#draw little circles round points
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
        self.buttons = Frame(self.master)#The ui is in its own little sub frame, to make sure it looks nice and everything lines up nicely.
        self.buttons.grid(row=0,column=0,sticky="NW")
        self.title = Label(self.buttons,text="Graph for PlayerID {0} named: {1}".format(playerID,playerName))
        self.title.grid(row=0,column=0,columnspan=2)
        self.averageLabel = Label(self.buttons,text="Average:")
        self.averageLabel.grid(row=2,column=0,sticky="E")
        self.average = Label(self.buttons,text=round(average,2))
        self.average.grid(row=2,column=1,sticky="W")
        self.newPlayerButton = Button(self.buttons, text="Graph on different player?", relief = GROOVE,command=self.playerNameChecker)
        self.newPlayerButton.grid(row=3,column=0,columnspan=2)
        #recent results
        self.recentResultsLabel = Label(self.buttons, text="Past 10 maps for this player")
        self.recentResultsLabel.grid(row=4,column=0,columnspan=2)
        self.recentResultsTree = Treeview(self.buttons)
        self.recentResultsTree.grid(row=5,column=0,columnspan=2)
        self.recentResultsTree["columns"]=("Rounds Won","Rounds Lost","Rating")
        self.recentResultsTree.column("#0", width=150, minwidth=150, stretch=NO)
        self.recentResultsTree.column("Rounds Won", width=100, minwidth=100, stretch=NO)
        self.recentResultsTree.column("Rounds Lost", width=100, minwidth=100, stretch=NO)
        self.recentResultsTree.column("Rating", width=50, minwidth=50, stretch=NO)
        self.recentResultsTree.heading("#0",text="Team Name")
        self.recentResultsTree.heading("Rounds Won",text="Rounds Won")
        self.recentResultsTree.heading("Rounds Lost",text="Rounds Lost")
        self.recentResultsTree.heading("Rating",text="Rating")
        cursor.execute("SELECT Team.TeamName, subqryRoundsWon, subqryRoundsLost, qryRating FROM (SELECT Nickname, TeamMap.TeamID TeamIDqry, Game.Date qryDate, TeamMap.RoundsWon subqryroundsLost, TeamMap.RoundsLost subqryroundsWon, PlayerMap.Rating qryRating FROM Player, PlayerMap, TeamMap, GameMap, Game WHERE Player.PlayerID = (?) AND Player.PlayerID = PlayerMap.PlayerID AND PlayerMap.GameMapID = TeamMap.GameMapID AND Player.TeamID != TeamMap.TeamID AND TeamMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) ),Team WHERE Team.TeamID = TeamIDqry ORDER BY qryDate DESC LIMIT 10;",(playerID, self.date90))
        un = 0
        for each in cursor.fetchall():
            splittedString = str(each).split(",")
            self.recentResultsTree.insert("", END, un, text=splittedString[0].split("'")[1], values=(splittedString[1],splittedString[2],splittedString[3].split(")")[0]))
            un = un+ 1
        #linear regression
        self.linRegBut = Button(self.buttons, text="Perform linear regression", relief = GROOVE, command= self.linRegSubrt)
        self.linRegBut.grid(row=6,column=0,columnspan=2)
        self.backButton = Button(self.buttons, text = "Main Menu", relief = GROOVE, command=self.graphToMainMenu)#On click goes to self.graphToMainMenu
        self.backButton.grid(row=7,column=0,columnspan=2)
    
    def linRegSubrt(self):#LinearRegression Subroutine.
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
        #y = bx+a
        sxy = sumXY-((sumX*sumY)/n)
        sxx = sumXSquared-(sumX**2/n)
        syy = sumYSquared-(sumY**2/n)
        b = sxy/sxx
        a=(sumY/n) - ((sumX/n)*b)
        self.pen3.penup()
        self.pen3.color("green")
        self.pen3.goto(-360,a+b*-360)
        self.pen3.pendown()
        print([360,a+b*-360])
        self.pen3.goto(360,a+b*360)
        self.pearsonsLabel = Label(self.buttons, text="PMCC:")
        self.pearsonsLabel.grid(row=7,column=0,columnspan=2)
        self.pearsons = Label(self.buttons, text = str(sxy/sqrt(sxx*syy)))
        self.pearsons.grid(row=8,column=0, columnspan=2)
        self.backButton.grid(row=9,column=0,columnspan=2)
    
    def playerNameChecker(self):
        self.buttons.destroy()
        self.canvas.destroy()
        self.playerSelector = Frame(self.master)
        self.playerSelector.grid()
        self.playerNicknameLabel = Label(self.playerSelector,text="Player Nickname:")
        self.playerNicknameEntry = Entry(self.playerSelector)
        self.playerNicknameEntry.focus()
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
        
        

def ui():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "CSGO-Results.db")
    mydb = sqlite3.connect(db_path)
    global cursor
    cursor = mydb.cursor()
    newDB = False
    if checkIfDatabaseExists() == False:#Because sqlite automatically creates a blank database file if no database file exists, the check we must make is to check all the tables.
        import buildDB
        newDB = True

    global root
    root = Tk() #makes a blank window

    app = Window(root)#Can hold other widgets
    app.mainMenu()
    #when creating a widget always pass its owner/master
    if newDB == True:
        messagebox.showinfo("Database Creation","This program was ran either without the database, or the program failed to find the database. The program has automatically made a database in place of this, but it wont have any data in it. This must be scraped.")
    root.mainloop()#Now awaits events to handle

def scraper():
    print("The scraper has been commented out.")
    #import SCRAPE

if __name__ == '__main__':
    scraperThread = Thread(target = scraper)# defining it as a variable so i can
    scraperThread.daemon = True# So i can make it a daemon thread
    scraperThread.start()# This means, if the ui closes, the scraper closes.

    ui()#keeping the GUI in the main thread
    #GUIs can sometimes behave strangely when on a thread
