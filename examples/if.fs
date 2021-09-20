__project__["mc-version"]  = "1.16.5"
__project__["name"]        = "if"
__project__["description"] = "A Demo"
__project__["author"]      = "FabulousFox"

class if: 
    def __load__():
        scoreboard("main")
        Player(selector="@p").main = 0
        if Player(selector="@p").main == 3:
            say("Score = 3")
            if Player(selector="@p").main == Player(selector="@p").main:
                say("sus")
