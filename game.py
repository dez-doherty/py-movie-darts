from types import MappingProxyType
from player import Player, GuessResult
from enum import Enum

class GameStatus(Enum):
    WAITING = 0
    IN_PROGRESS = 1
    FINISHED = 2

class Game:
    def __init__(self, config):
        self.players = {}
        self.config = MappingProxyType(config)
        self.winner = {"player": None, "points": float("-inf")}
        self.game_status = GameStatus.WAITING



    def add_player(self, name):
        if self.game_status != GameStatus.WAITING: return
        self.players[name] = Player(name, self)

    def get_player(self, name):
        return self.players[name]
    

    
    def set_winner(self, player):
        if self.game_status != GameStatus.IN_PROGRESS: return
        self.winner = {"player": player, "points": player.points}

    def declare_winner(self, winner):
        if self.game_status != GameStatus.IN_PROGRESS: return
        self.end_game()
        print(f"{winner.name} won the game with {winner.points} points ")



    def start_game(self):
        if self.game_status != GameStatus.WAITING: return
        self.game_status = GameStatus.IN_PROGRESS

    def end_game(self):
        if self.game_status != GameStatus.IN_PROGRESS: return
        self.game_status = GameStatus.FINISHED