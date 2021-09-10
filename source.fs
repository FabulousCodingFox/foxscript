__project__["mc-version"]  = "1.16.5"
__project__["name"]        = "Fox"
__project__["description"] = "FoxSciptTest"
__project__["author"]      = "FabulousFox"

class Main: 
    def __tick__():
        say("Main.Tick")
    def __load__():
        scoreboard("main")
        if Player("DerRote123").main == 3:
            say("Score = 3")
        if 2==Player("DerRote123").main:
            say("Score = 2")