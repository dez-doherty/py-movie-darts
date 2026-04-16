from classes.player import *
from configs.configs import *

class Game:
    def __init__(self, players, stat, cat_option):
        self.players = players
        self.stat = stat
        self.cat_option = cat_option

    def run(self):
        active_players = self.players.copy()
        
        while active_players:
            for player in active_players.copy():
                print(f"\n{player.name}'s turn — Score: {player.score}")
                guess = input("Guess: ")
                
                if guess.lower() == "quit":
                    print(f"{player.name} has left the game!")
                    active_players.remove(player)
                    continue
                
                _, message = player.guess(guess, self.stat, self.cat_option)
                print(message)
            
            if not active_players:
                print("No players remaining, game over!")
                return

            in_checkout = [p for p in active_players if 0 <= p.score <= MAX_BUST]
            
            if in_checkout:
                winner_score = min(p.score for p in in_checkout)
                winners = [p for p in in_checkout if p.score == winner_score]
                
                if len(winners) == 1:
                    print(f"\n{winners[0].name} wins with a score of {winners[0].score}!")
                else:
                    names = ", ".join(w.name for w in winners)
                    print(f"\nIt's a tie between {names} with a score of {winner_score}!")
                return