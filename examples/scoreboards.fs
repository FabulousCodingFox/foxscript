class Main:
    def __load__():
        scoreboard("points")
        Player(selector="@p",name="Steve").points = 100
    def __tick__():
        Player(selector="@p",name="Steve").points += 10
        Player(selector="@p",name="Steve").points *= Player(selector="@p",name="Alex").points
