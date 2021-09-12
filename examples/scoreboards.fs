__project__["mc-version"]  = "1.16.5"
__project__["name"]        = "scoreboards"
__project__["description"] = "Scoreboard example"
__project__["author"]      = "FabulousFox"

class scoreboards: 
    def __tick__():
        Player().main+=1#Adding 1 to main for everyone
    def __load__():
        scoreboard("main")#Creating the scoreboard "main"
        Player().main = 5#Setting the Scoreboard for everyone to 5
        setdisplay("main")#Displaying the scoreboard
