from tkinter import *
import sqlite3,turtle
from datetime import date, timedelta, datetime
mydb = sqlite3.connect("CSGO-Results.db")
cursor = mydb.cursor()

class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)# Use the constructor
        #OR super().__init__(master)
        self.master = master

        self.master.title("Program name")
        self.date = date.today() - timedelta(90)
        self.grid(row=0,column=0)
        
    def mainMenu(self):
        self.eventMvpPicker = Button(self, text = "Event MVP Picker")
        self.eventMvpPicker.grid(row=1,column=0)
        self.teamsOnRise = Button(self, text = "Players on the Rise")
        self.teamsOnRise.grid(row=2,column=0)
        self.line = Label(self, text = "LINE")
        self.line.grid(row=0,column=1)
        self.lab1 = Label(self, text = "Performing players")
        cursor.execute("SELECT subqry.PlayerID, round(subqry.AVERAGERATING,2), subqry.MAPCOUNT FROM (SELECT PlayerID, avg(Rating) AVERAGERATING,COUNT(Rating) MAPCOUNT FROM PlayerMap, GameMap,Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) GROUP BY PlayerID)AS subqry WHERE subqry.AVERAGERATING>1.3 AND subqry.MAPCOUNT > 10",(str(self.date),))
        self.qry1 = cursor.fetchall()
        cursor.execute("SELECT subqry.PlayerID, round(subqry.AVERAGERATING,2), subqry.MAPCOUNT FROM (SELECT PlayerID, avg(Rating) AVERAGERATING,COUNT(Rating) MAPCOUNT FROM PlayerMap, GameMap,Game WHERE PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) GROUP BY PlayerID)AS subqry WHERE subqry.AVERAGERATING<0.75 AND subqry.MAPCOUNT > 10",(str(self.date),))
        self.qry2 = cursor.fetchall()
        self.lab1.grid(row=1,column=3)
        self.improvPlayersL = Listbox(self,height = (len(self.qry1)+1))
        self.improvPlayersL.grid(row=2,column=2)
        self.improvPlayersL.insert(1, "Player Name")
        self.improvPlayersM = Listbox(self,height = (len(self.qry1)+1))
        self.improvPlayersM.grid(row=2, column=3)
        self.improvPlayersM.insert(1, "Num Maps")
        self.improvPlayersR = Listbox(self,height = (len(self.qry1)+1))
        self.improvPlayersR.grid(row=2, column=4)
        self.improvPlayersR.insert(1, "Rating")
        for i in range (len(self.qry1)):
            cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(int(self.qry1[i][0]),))
            self.improvPlayersL.insert(i+2, str(cursor.fetchall()[0][0]))
            self.improvPlayersM.insert(i+2, str(self.qry1[i][2]))
            self.improvPlayersR.insert(i+2,str(self.qry1[i][1]))
        self.lab2 = Label(self, text = "Underperforming players")
        self.lab2.grid(row=3,column=3)
        self.underPlayersL = Listbox(self,height = (len(self.qry2)+1))
        self.underPlayersL.grid(row=4,column=2)
        self.underPlayersL.insert(1, "Player Name")
        self.underPlayersM = Listbox(self,height = (len(self.qry2)+1))
        self.underPlayersM.grid(row=4, column=3)
        self.underPlayersM.insert(1, "Num Maps")
        self.underPlayersR = Listbox(self,height = (len(self.qry2)+1))
        self.underPlayersR.grid(row=4, column=4)
        self.underPlayersR.insert(1, "Rating")
        for i in range (len(self.qry2)):
            cursor.execute("SELECT Nickname FROM Player WHERE PlayerID = (?)",(int(self.qry2[i][0]),))
            self.underPlayersL.insert(i+2, str(cursor.fetchall()[0][0]))
            self.underPlayersM.insert(i+2, str(self.qry2[i][2]))
            self.underPlayersR.insert(i+2,str(self.qry2[i][1]))
        self.selectPlayerButton = Button(self,text="Select Player",command = self.testtt)
        self.selectPlayerButton.grid(row=5,column=3)

#listbox

    def testtt(self):
        if len(self.improvPlayersL.curselection()) > 0 and self.improvPlayersL.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersL.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        elif len(self.improvPlayersM.curselection()) > 0 and self.improvPlayersM.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersM.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        elif len(self.improvPlayersR.curselection()) > 0 and self.improvPlayersR.curselection()[0] != 0:
            playerID = (self.qry1[self.improvPlayersR.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        #underperforimg players
        elif len(self.underPlayersL.curselection()) > 0 and self.underPlayersL.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersL.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        elif len(self.underPlayersM.curselection()) > 0 and self.underPlayersM.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersM.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        elif len(self.underPlayersR.curselection()) > 0 and self.underPlayersR.curselection()[0] != 0:
            playerID = (self.qry2[self.underPlayersR.curselection()[0]-1][0])
            self.destroyMainMenu()
            self.graph(playerID)
        else:
            print("YOU HAVENT SELECTED ANYHTING BITHC.")

    def destroyMainMenu(self):
        self.eventMvpPicker.destroy()
        self.teamsOnRise.destroy()
        self.line.destroy()
        self.lab1.destroy()
        self.lab2.destroy()
        self.improvPlayersL.destroy()
        self.improvPlayersM.destroy()
        self.improvPlayersR.destroy()
        self.underPlayersL.destroy()
        self.underPlayersM.destroy()
        self.underPlayersR.destroy()
        self.selectPlayerButton.destroy()
        

    def graph(self,playerID):
        print(playerID)
            
        cursor.execute("SELECT Game.Date, Rating FROM PlayerMap, GameMap, Game WHERE PlayerID = (?) AND PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > (?) ORDER BY Date DESC",(playerID,str(self.date)))
        playerRatings = cursor.fetchall()
        average =0.0
        playerRatingsDate = []
        num = len(playerRatings)
        coords = []
        for i in range(len(playerRatings)):
            average += float(playerRatings[i][1])
            print((((int((str(datetime.strptime(playerRatings[i][0],'%Y-%m-%d').date()- self.date)).split(" day")[0])-90)*-1)-45)*8)
            playerRatingsDate.append((((int((str(datetime.strptime(playerRatings[i][0],'%Y-%m-%d').date()- self.date)).split(" day")[0])-90)*-1)-45)*8)
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
            coords.append([playerRatingsDate[temp],((tempnumber/len(templist))-1)*300])
            temp += int(outputstring[i])
        average = average/len(playerRatings)
        print(average)
        avgcoords = [[-400,(average-1)*300],[400,(average-1)*300]]
        
        ##### setup #######
        h,w=600,720
        canvas=Canvas(master=root,height=h,width=w)
        pen=turtle.RawTurtle(canvas)
        pen2=turtle.RawTurtle(canvas)
        pen3=turtle.RawTurtle(canvas)
        pen.hideturtle()
        pen2.hideturtle()
        pen3.hideturtle()
        pen.speed(0)
        pen2.speed(0)
        pen3.speed(0)
        pen2.color("blue")
        pen3.color("red")
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
        ########  coords  #################
        pen2.penup()
        for i in coords:
            pen2.goto(i)
            pen2.pendown()
        pen3.penup()
        for i in avgcoords:
            pen3.goto(i)
            pen3.pendown()
        canvas.grid(row=0,column=1)

        ###### UI Around Graph ############################
        self.buttons = Frame(self.master,width=0)
        self.buttons.grid(row=0,column=0,sticky="NW")
        self.testLab = Label(self.buttons,text="TESSTTT")
        self.testLab.grid(row=0,column=0)
        self.title = Label(self.buttons,text="Helloooooo graphhh")
        self.title.grid(row=0,column=1)
        self.averageLabel = Label(self.buttons,text="Average:")
        self.averageLabel.grid(row=2,column=0,sticky="E")
        self.average = Label(self.buttons,text=average)
        self.average.grid(row=2,column=1,sticky="W")
        self.backButton = Button(self.buttons, text = "Back" )
        self.backButton.grid(row=3,column=1)

    def window(self):# new seperate window.
        window = Toplevel(self.master)
        


root = Tk() #makes a blank window
##root.geometry("512x512")#Dimensions of window

app = Window(root)#Can hold oter widgets
app.mainMenu()
#when creating a widget always pass its owner/master
root.mainloop()#Now awaits events to handle
