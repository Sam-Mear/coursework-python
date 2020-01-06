from tkinter import *

class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)# Use the constructor
        #OR super().__init__(master)
        self.master = master

        self.master.title("Program name")
        self.grid()
        
    def mainMenu(self):
        self.eventMvpPicker = Button(self, text = "Event MVP Picker")
        self.eventMvpPicker.grid(row=1,column=0)
        self.teamsOnRise = Button(self, text = "Teams on the Rise")
        self.teamsOnRise.grid(row=2,column=0)
        self.line = Label(self, text = "LINE")
        self.line.grid(row=0,column=1)
        self.lab1 = Label(self, text = "Noteable results list")
        self.lab1.grid(row=0,column=3)
        self.resultsListL = Listbox(self)
        self.resultsListL.grid(row=1,column=2)
        self.resultsListL.insert(1, "Team 1 ")
        self.resultsListM = Listbox(self)
        self.resultsListM.grid(row=1, column=3)
        self.resultsListM.insert(1, "Team 2")
        self.resultsListR = Listbox(self)
        self.resultsListR.grid(row=1, column=4)
        self.resultsListR.insert(1, "Result")
        self.lab2 = Label(self, text = "Improving players")
        self.lab2.grid(row=2,column=3)
        self.improvPlayersL = Listbox(self)
        self.improvPlayersL.grid(row=3,column=2)
        self.improvPlayersL.insert(1, "Player Name")
        self.improvPlayersM = Listbox(self)
        self.improvPlayersM.grid(row=3, column=3)
        self.improvPlayersM.insert(1, "Team Name")
        self.improvPlayersR = Listbox(self)
        self.improvPlayersR.grid(row=3, column=4)
        self.improvPlayersR.insert(1, "Rating")
        self.lab2 = Label(self, text = "Underperforming players")
        self.lab2.grid(row=4,column=3)
        self.underPlayersL = Listbox(self)
        self.underPlayersL.grid(row=5,column=2)
        self.underPlayersL.insert(1, "Player Name")
        self.underPlayersM = Listbox(self)
        self.underPlayersM.grid(row=5, column=3)
        self.underPlayersM.insert(1, "Team Name")
        self.underPlayersR = Listbox(self)
        self.underPlayersR.grid(row=5, column=4)
        self.underPlayersR.insert(1, "Rating")

#listbox

    def window(self):# new seperate window.
        window = Toplevel(self.master)
        
##    def teamToMainMenu(self):
##        self.lab1.destroy()
##        self.inp.destroy()
##        self.lab2.destroy()
##        self.temp1.destroy()
##        self.temp2.destroy()
##        self.lab3.destroy()
##        self.lab4.destroy()
##        self.temp3.destroy()
##        self.temp4.destroy()
##        self.b1.destroy()
##        self.mainMenu()
##    def regTeam(self):
##        self.b1.destroy()
##        self.b2.destroy()
##        self.b3.destroy()
##        self.b4.destroy()
##        self.lab1 = Label(self, text = "Team Name:")
##        self.lab1.grid(row=0,column = 0)
##        self.inp = Entry(self)
##        self.inp.grid(row=0,column=1)
##        self.lab2 = Label(self,text = "Individual or Team?")
##        self.lab2.grid(row=1,column=0)
##        
##        self.temp1 = Label(self,text="Individual")
##        self.temp1.grid(row=2,column=0)
##        self.temp2 = Label(self,text="Team")
##        self.temp2.grid(row=3,column=0)
##
##        self.lab3 = Label(self,text="Only for a few events?")
##        self.lab3.grid(row=4,column=0)
##        self.lab4 = Label(self,text="Excludes them from the main leaderboard")
##        self.lab4.config(font=("Calibri", 7))
##        self.lab4.grid(row=5,column=0)
##        
##        self.temp3 = Label(self, text="Yes")
##        self.temp3.grid(row=6,column=0)
##        self.temp4 = Label(self, text="No")
##        self.temp4.grid(row=7, column=0)
##        
##        self.b1 = Button(self, text = "Submit", command = self.teamToMainMenu)
##        self.b1.grid(row=8, column = 0)
##    def recEvent(self):
##        self.b1.destroy()
##        self.b2.destroy()
##        self.b3.destroy()
##        self.b4.destroy()
##        self.lab1= Label(self, text="Select event name:")
##        self.lab1.grid(row=0,column=0)
        


root = Tk() #makes a blank window
##root.geometry("512x512")#Dimensions of window

app = Window(root)#Can hold oter widgets
app.mainMenu()
#when creating a widget always pass its owner/master
root.mainloop()#Now awaits events to handle
