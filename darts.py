from types import MappingProxyType
from player import Player, GuessResult
from game import Game, GameStatus
from enum import Enum

class Darts(Game):
    def __init__(self, config):
        super().__init__(config)
        self.rounds = 0
        self.current_visitor = None

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
        super().start_game()

        while self.game_status == GameStatus.IN_PROGRESS:
            self.rounds += 1
            for _, player in self.players.items():
                self.set_turn(player)
            self.end_round()
    
    def end_round(self):
        if self.game_status != GameStatus.IN_PROGRESS: return

        winner = self.winner["player"]
        if winner:
            self.declare_winner(winner)