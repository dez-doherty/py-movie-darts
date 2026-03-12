from types import MappingProxyType
from player import Player, GuessResult
from enum import Enum

class GameStatus(Enum):
    WAITING = 0
    IN_PROGRESS = 1
    FINISHED = 2

BUST_THRESHOLD = -10

class Round:
    def __init__(self, config):
        self.players = {}
        self.current_visitor = None
        self.rounds = 0
        self.config = MappingProxyType(config)
        self.winner = {"player": None, "points": float("-inf")}
        self.game_status = GameStatus.WAITING

    def set_turn(self, player):
        if self.game_status != GameStatus.IN_PROGRESS: return

        self.current_visitor = player
        player.visits += 1

        answer = input(f"{player.name}'s turn: you have {player.points} points. ")
        score, status = player.guess(answer)

        print(f"{player.name}: '{answer}' = {score};", end = " ")

        if status == GuessResult.CHECK_OUT:
            print(f"checked out at {player.points},", end = " ")

            if player.points > self.winner["points"]:
                if player.points == 0:
                    self.declare_winner(player) 
                    return
                elif player.points < 0:
                    self.set_winner(player)
                    print(f"0 to {player.points + 1} points to win ")
            else:
                print("cannot win")

        elif status == GuessResult.SCORE:
            print(f"{player.points} remaining ")
        elif status == GuessResult.BUST:
            print(f"BUST, remains at {player.points} ")
        elif status == GuessResult.ILLEGAL:
            print(f"ILLEGAL, remains at {player.points} ")



    def start_game(self):
        if self.game_status != GameStatus.WAITING: return

        while not self.game_status == GameStatus.IN_PROGRESS:
            self.rounds += 1
            for _, player in self.players.items():
                self.set_turn(player)
            self.end_round()
    
    def end_round(self):
        if self.game_status != GameStatus.IN_PROGRESS: return

        winner = self.winner["player"]
        if winner:
            self.declare_winner(winner)
            print(f"{winner.name} won the game with {winner.points} points ")

    def end_game(self):
        if self.game_status != GameStatus.FINISHED: return
        self.game_status = GameStatus.FINISHED
        print("Game ended")
        


    def set_winner(self, player):
        self.winner = {"player": player, "points": player.points}

    def declare_winner(self, player):
        self.set_winner(player)
        self.end_game()



    def add_player(self, name):
        self.players[name] = Player(name, self)

    def get_player(self, name):
        return self.players[name]