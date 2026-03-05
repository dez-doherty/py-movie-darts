from types import MappingProxyType
from player import Player, GuessResult

BUST_THRESHOLD = -10

class Round:
    def __init__(self, config):
        self.players = {}
        self.current_visitor = None
        self.rounds = 0
        self.config = MappingProxyType(config)
        self.winner = {"player": None, "points": float("-inf")}
        self.game_over = False

    def add_player(self, name):
        self.players[name] = Player(name, self)

    def set_turn(self, player):
        self.current_visitor = player
        player.visits += 1

        answer = input(f"{player.name}'s turn: you have {player.points} points. ")
        score, status = player.guess(answer)

        print(f"{player.name}: '{answer}' = {score};", end = " ")

        if status == GuessResult.CHECK_OUT:
            print(f"checked out at {player.points},", end = " ")

            if player.points > self.winner["points"]:
                if player.points == 0:

                elif player.points < 0:
                    self.winner = {"player": player, "points": player.points}
                    print(f"0 to {player.points + 1} points to win ")
            else:
                print("cannot win")

        elif status == GuessResult.SCORE:
            print(f"{player.points} remaining ")
        elif status == GuessResult.BUST:
            print(f"BUST, remains at {player.points} ")
        elif status == GuessResult.ILLEGAL:
            print(f"ILLEGAL, remains at {player.points} ")
            
    def start(self):
        while not self.game_over:
            self.rounds += 1
            for _, player in self.players.items():
                self.set_turn(player)
            self.end_round()
        
    def end_round(self):
        self.game_over = True
        
        winner = self.winner["player"]
        if winner:
            self.declare_winner(winner)
            print(f"{winner.name} won the game with {winner.points} points ")

    def declare_winner(self, player):
        print(f"Game over! {player.name} wins! ")

    def get_player(self, name):
        return self.players[name]