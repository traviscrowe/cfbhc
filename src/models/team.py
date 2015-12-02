class Team(object):
    def _init_(self, players):
        self.players = players

    def getPlayersAtPosition(position):
        pos_players = []
        for player in self.players:
            if(player.position == position):
                pos_players.append(player)
        return pos_players

    def getOffensiveLineRating():
        ot = getPlayersAtPosition("OT")
        og = getPlayersAtPosition("OG")
        c = getPlayersAtPosition("C")
        
